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

    def __init__(self, base_dir: Path, output_root: Path):
        super().__init__()
        self.base_dir = base_dir
        self.output_root = output_root

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

    def _modify_json_content(self, rec: dict, user: str, experiment: str, log_filename: str):
        """Modify JSON content to use actual user and experiment names."""
        # Update data_product_id and experiment_name to use experiment folder name
        rec["data_product_id"] = experiment
        rec["experiment_name"] = experiment
        
        # Update username and calc_by to use actual user name
        rec["username"] = user
        if "execution_environment" in rec and "calc_by" in rec["execution_environment"]:
            rec["execution_environment"]["calc_by"] = user
        
        # Update indexed_time to current time when processing
        rec["indexed_time"] = int(time.time() * 1000)  # Convert to milliseconds
        
        # Update files section to use log filename instead of "job"
        if "files" in rec:
            log_stem = Path(log_filename).stem  # Get filename without extension
            rec["files"] = {
                "smiles_file": f"{log_stem}_smiles.txt",
                "sdf_structure_file": f"{log_stem}_structure.sdf",
                "gaussian_output_file": f"../{log_filename}",
                "gaussian_input_file": f"{log_stem}.gjf",
                "pdb_structure_file": f"{log_stem}_structure.pdb",
                "inchi_file": f"{log_stem}_inchi.txt",
                "gaussian_checkpoint_file": "",
                "gaussian_f_checkpoint_file": ""
            }

    def _rename_job_files(self, parsed_dir: Path, log_stem: str):
        """Renames job_* files to log_stem_* files if they exist."""
        # Define file mappings: job_* -> log_stem_*
        file_mappings = {
            "job.json": f"{log_stem}.json",
            "job_smiles.txt": f"{log_stem}_smiles.txt",
            "job_structure.sdf": f"{log_stem}_structure.sdf",
            "job.gjf": f"{log_stem}.gjf",
            "job_structure.pdb": f"{log_stem}_structure.pdb",
            "job_inchi.txt": f"{log_stem}_inchi.txt",
            "job_temp.png": f"{log_stem}_temp.png",
            "job_temp.sdf": f"{log_stem}_temp.sdf"
        }
        
        for job_file in parsed_dir.glob("job_*"):
            if job_file.name in file_mappings:
                new_name = file_mappings[job_file.name]
                try:
                    job_file.rename(parsed_dir / new_name)
                    print(f"Renamed {job_file.name} to {new_name}")
                except FileExistsError:
                    print(f"Skipping rename for {job_file.name} to {new_name} due to conflict.")
                except Exception as e:
                    print(f"Error renaming {job_file.name} to {new_name}: {e}")

    def on_created(self, event):
        p = Path(str(event.src_path))
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
        experiment = log_path.parent.name          # 例如 "exp001"
        log_stem = log_path.stem                   # log文件名（不含扩展名）
        
        # 为每个log文件创建独立的输出文件夹
        parsed_dir = self.output_root / user / experiment / log_stem
        parsed_dir.mkdir(parents=True, exist_ok=True)

        user_opts = []
        if hasattr(os, "getuid"):
            user_opts = ["--user", f"{os.getuid()}:{os.getgid()}"]

        # 使用log文件名作为Docker输入文件名
        proc = subprocess.run([
            "docker", "run", "--rm",
            "-w", "/data/output",
            *user_opts,
            "-v", f"{log_path}:/data/input/job.log:ro",
            "-v", f"{parsed_dir}:/data/output",
            DOCKER_IMG,
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if proc.returncode != 0:
            print(f"✗ Docker parser failed for {log_path}\n{proc.stderr}")
            return

        # Rename job_* files to log_stem_* files
        self._rename_job_files(parsed_dir, log_stem)

        candidate = [
            parsed_dir / "gaussian.json",
            parsed_dir / "job.json",
            parsed_dir / f"{log_stem}.json",
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

        target_json = parsed_dir / f"{log_stem}.json"
        if json_path != target_json and not target_json.exists():
            json_path.rename(target_json)
            json_path = target_json

        with open(json_path, encoding="utf-8") as fp:
            raw = json.load(fp)

        records = raw if isinstance(raw, list) else [raw]
        
        # Modify JSON content before uploading
        for rec in records:
            self._modify_json_content(rec, user, experiment, log_path.name)
        
        # Write modified JSON content back to file
        with open(json_path, 'w', encoding="utf-8") as fp:
            json.dump(records if len(records) > 1 else records[0], fp, indent=2)
        
        req = {"user_id": user, "tenant_id": "demotenant", "group_ids": []}
        catalog = DataCatalogService(req)
        dp_type = smiles_dp_util.SmilesDP.COMPUTATIONAL

        uploaded = []
        for rec in records:
            try:
                smiles_dp = smiles_dp_util.get_smiles_dp(dp_type, rec)
                catalog_dp = smiles_dp_util.map_smiles_dp_to_catalog_dp(req, smiles_dp, dp_type)
                res = catalog.create_data_product(catalog_dp)
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
        parser.add_argument(
            "--output_dir",
            default=os.getenv("SMILES_OUTPUT_DIR", "/data/smiles"),
            help="Directory where parsed JSON will be written.",
        )
        parser.add_argument(
            "--force_reprocess",
            action="store_true",
            help="Force reprocessing of all log files by removing .uploaded files first.",
        )

    def handle(self, *args, **opts):
        base_dir = Path(opts["base_dir"]).expanduser().resolve()
        output_dir = Path(opts["output_dir"]).expanduser().resolve()
        if not base_dir.exists():
            raise CommandError(f"Base directory '{base_dir}' does not exist")
        output_dir.mkdir(parents=True, exist_ok=True)

        # If force_reprocess is enabled, remove all .uploaded files first
        if opts.get("force_reprocess"):
            self.stdout.write("Force reprocessing enabled. Removing all .uploaded files...")
            uploaded_files_removed = 0
            for uploaded_file in base_dir.rglob("*.uploaded"):
                uploaded_file.unlink()
                uploaded_files_removed += 1
            self.stdout.write(f"Removed {uploaded_files_removed} .uploaded files.")

        handler = LogHandler(base_dir, output_dir)

        for log_path in base_dir.rglob("*.log"):
            if not handler._already_processed(log_path):
                handler.handle_log(log_path)

        observer = Observer()
        observer.schedule(handler, str(base_dir), recursive=True)
        observer.start()
        self.stdout.write(f"Watcher started at {base_dir}")

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()