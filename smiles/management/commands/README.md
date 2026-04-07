# SMILES Log Watcher

This tool automatically watches Gaussian `.log` files under SMILES user folders, parses them via Docker, and uploads the generated JSON to the Airavata Data Catalog.

The parsed JSON files are saved to `/data/smiles/<username>/<experiment_name>/<log_filename>/` by default. Each log file gets its own output folder to avoid conflicts. You can customize this output location with the `--output_dir` option.

## Features

- **Automatic file organization**: Each log file generates files in its own folder named after the log file
- **Smart file naming**: Generated files use the log filename instead of hardcoded "job" names
- **User and experiment detection**: Automatically detects user and experiment names from folder structure
- **Force reprocessing**: Option to reprocess all files by removing upload markers
- **Real-time monitoring**: Watches for new log files and processes them automatically

## Setup

Navigate to the airavata-django-portal directory:

```bash
cd airavata-django-portal
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

**Windows note:** Use the following command instead:

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install watchdog
```

## Pull Docker Image

```bash
docker pull miao0703/gaussian-parser:1.0
```

## Usage

To monitor the default input path `/var/www/portals/gateway-user-data/smiles` and save parsed results under `/data/smiles`:
```bash
python manage.py watch_logs
```

To watch a custom path:

```bash
python manage.py watch_logs \
  --base_dir /your/input/path \
  --output_dir /your/output/path
```

To force reprocessing of all log files (removes existing upload markers):

```bash
python manage.py watch_logs --force_reprocess
```

To run in background:

```bash
nohup python manage.py watch_logs > watcher.log 2>&1 &
```

## Parameters

- `--base_dir`: Base directory where SMILES user folders live (default: `/var/www/portals/gateway-user-data/smiles`)
- `--output_dir`: Directory where parsed JSON will be written (default: `/data/smiles`)
- `--force_reprocess`: Force reprocessing of all log files by removing `.uploaded` files first

## Output Structure

For a log file at `/path/to/smiles/user1/experiment1/1.log`, the output will be:
```
/data/smiles/user1/experiment1/1/
├── 1.json
├── 1_smiles.txt
├── 1_structure.sdf
├── 1.gjf
├── 1_structure.pdb
└── 1_inchi.txt
```