# SMILES Log Watcher

This tool automatically watches Gaussian `.log` files under SMILES user folders, parses them via Docker, and uploads the generated JSON to the Airavata Data Catalog.

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

To monitor the default path `/var/www/portals/gateway-user-data/smiles`:

```bash
python manage.py watch_logs
```

To watch a custom path:

```bash
python manage.py watch_logs --base_dir /your/custom/path
```

To run in background:

```bash
nohup python manage.py watch_logs > watcher.log 2>&1 &
```