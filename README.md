# smiles-django-portal
A Portal to support SMILES Project

1.  Checkout this project and create a virtual environment.

    ```
    git clone https://github.com/lahirujayathilake/smiles-django.git
    cd smiles-django
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    ```

2.  Follow the instructions and run Apache Airavata Data Catalog - https://github.com/apache/airavata-data-catalog

3.  Run the Django application

    ```
    python manage.py runserver
    ```

4.  Run the Redis Server

    ```
    redis-server
    ```

5.  Run Celery worker

    ```
    python -m celery -A smiles_django worker -l info
    ```