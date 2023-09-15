# SMILES Django Portal

## Getting Started

A Portal to support SMILES Project

1. Follow the instructions for installing the
   [Airavata Django Portal](https://github.com/apache/airavata-django-portal)

2. settings.py file

	For the correct operation of this Django project, the following configurations should be added to your `settings.py` file:
	
	```
	# Max upload size is set to 2GB
	FILE_UPLOAD_MAX_FILE_SIZE = 1024 * 1024 * 1024 * 2
	
	# Celery settings
	CELERY_BROKER_URL = "redis://localhost:6379"
	CELERY_RESULT_BACKEND = "redis://localhost:6379"
	```

3. To build the frontend, navigate to `smiles-django-portal/frontend` and run
	
	```
	yarn run build
	```

4. With the Airavata Django Portal virtual environment activated, clone this
   repo and install it into the portal's virtual environment

   ```
   cd smiles-django-portal
   pip install -e .
   ```

5. Start (or restart) the Django Portal server.
   ```
   python manage.py runserver
   ```

6. Run the Redis Server

   ```
   redis-server
   ```

7. Run Celery worker

   ```
   python -m celery -A smiles worker -l info
   ```

8. Follow the instructions and run Apache Airavata Data Catalog - https://github.com/apache/airavata-data-catalog