import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_airavata.settings")
app = Celery("smiles_django")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
