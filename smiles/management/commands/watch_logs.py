import os
import json
import time
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from smiles import smiles_dp_util
from smiles.data_catalog_service import DataCatalogService

DOCKER_IMG = "miao0703/gaussian-parser:1.0"


class LogHandler(FileSystemEventHandler):

    def __init__(self, base_dir: Path):
        super().__init__()
        self.base_dir = base_dir

    @staticmethod
    def _wait_until_stable(path: Path, timeout: float = 10.0, step: float = 0.5) -> bool:
        elapsed = 0.0
        last_size = -1
        while elapsed < timeout:
            size = path.stat().st_size
            if size == last_size and size > 0:
                return True
            last_size = size
            time.sleep(step)
            elapsed += step
        return False

    def _find_user_dir(self, log_path: Path) -> Path:
        for parent in log_path.parents:
            if parent.parent == self.base_dir:
                return parent
        return log_path.parents[2]

    def _already_processed(self, log_path: Path) -> bool:
        return log_path.with_suffix(".uploaded").exists()

    def on_created(self, event):
        p = Path(event.src_path)
        if p.is_file() and p.suffix == ".log":
            self.handle_log(p)

    def handle_log(self, log_path: Path):
        if self._already_processed(log_path):
            print(f"• skip (already uploaded): {log_path}")
            return

        if not self._wait_until_stable(log_path):
            print(f"✗ Timed out waiting for {log_path} to finish writing")
            return

        user_dir = self._find_user_dir(log_path)
        user = user_dir.name
        parsed_dir = log_path.parent / log_path.stem
        parsed_dir.mkdir(exist_ok=True)

        user_opts = []
        if hasattr(os, "getuid"):
            user_opts = ["--user", f"{os.getuid()}:{os.getgid()}"]

        proc = subprocess.run([
            "docker", "run", "--rm", *user_opts,
            "-v", f"{log_path}:/data/input/job.log:ro",
            "-v", f"{parsed_dir}:/data/output",
            DOCKER_IMG,
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if proc.returncode != 0:
            print(f"✗ Docker parser failed for {log_path}\n{proc.stderr}")
            return

        candidate = [
            parsed_dir / "gaussian.json",
            parsed_dir / "job.json",
            parsed_dir / f"{log_path.stem}.json",
            ]
        json_path = next((p for p in candidate if p.exists()), None)
        if json_path is None:
            for _ in range(10):
                jsons = list(parsed_dir.glob("*.json"))
                if jsons:
                    json_path = jsons[0]
                    break
                time.sleep(0.5)
        if json_path is None or not json_path.exists():
            print(f"✗ Parser did not generate JSON for {log_path}")
            return

        target_json = parsed_dir / f"{log_path.stem}.json"
        if json_path != target_json and not target_json.exists():
            json_path.rename(target_json)
            json_path = target_json

        with open(json_path, encoding="utf-8") as fp:
            raw = json.load(fp)

        records = raw if isinstance(raw, list) else [raw]
        req = {"user_id": user, "tenant_id": "demotenant", "group_ids": []}
        catalog = DataCatalogService(req)
        dp_type = smiles_dp_util.SmilesDP.COMPUTATIONAL

        uploaded = []
        for rec in records:
            try:
                smiles_dp = smiles_dp_util.get_smiles_dp(dp_type, rec)
                catalog_dp = smiles_dp_util.map_smiles_dp_to_catalog_dp(req, smiles_dp, dp_type)
                res = catalog.create_data_product(catalog_dp)
                if hasattr(smiles_dp_util, "add_dp_to_schemas"):
                    smiles_dp_util.add_dp_to_schemas(req, res)
                uploaded.append(res.data_product_id)
            except Exception as e:
                print(f"✗ Upload failed for {log_path}: {e}")

        if not uploaded:
            return

        sentinel = log_path.with_suffix(".uploaded")
        sentinel.write_text("\n".join(uploaded))
        print("✓ uploaded", ", ".join(uploaded))

class Command(BaseCommand):
    help = "Watch SMILES user-data tree, parse new *.log files and upload JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--base_dir",
            default=os.getenv("SMILES_BASE_DIR", "/var/www/portals/gateway-user-data/smiles"),
            help="Base directory where SMILES user folders live.",
        )

    def handle(self, *args, **opts):
        base_dir = Path(opts["base_dir"]).expanduser().resolve()
        if not base_dir.exists():
            raise CommandError(f"Base directory '{base_dir}' does not exist")

        handler = LogHandler(base_dir)

        for log_path in base_dir.rglob("*.log"):
            if not handler._already_processed(log_path):
                handler.handle_log(log_path)

        observer = Observer()
        observer.schedule(handler, str(base_dir), recursive=True)
        observer.start()
        self.stdout.write(self.style.SUCCESS(f"Watcher started at {base_dir}"))

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()