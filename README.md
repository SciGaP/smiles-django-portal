# SMILES Django Portal

## Getting Started

A Portal to support SMILES Project

1. Follow the instructions for installing the
   [Airavata Django Portal](https://github.com/apache/airavata-django-portal)
2. With the Airavata Django Portal virtual environment activated, clone this
   repo and install it into the portal's virtual environment

   ```
   cd smiles-django-portal
   pip install -e .
   ```

3. Start (or restart) the Django Portal server.
   ```
   python manage.py runserver
   ```

4. Run the Redis Server

   ```
   redis-server
   ```

5. Run Celery worker

   ```
   python -m celery -A smiles_django worker -l info
   ```

6. Follow the instructions and run Apache Airavata Data Catalog - https://github.com/apache/airavata-data-catalog