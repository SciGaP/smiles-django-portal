from django.apps import AppConfig
from celery import Celery
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_airavata.settings")
celery_app = Celery("smiles")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")


class Settings:
    WEBPACK_LOADER = {
        "SMILES": {
            "BUNDLE_DIR_NAME": "smiles/dist/",  # must end with slash
            "STATS_FILE": os.path.join(
                BASE_DIR,
                "static",
                "smiles",
                "dist",
                "webpack-stats.json",
            ),
        }
    }


class SmilesDjangoPortalConfig(AppConfig):
    # Standard Django app configuration. For more information on these settings,
    # see https://docs.djangoproject.com/en/2.2/ref/applications/#application-configuration
    name = 'smiles'
    label = name
    verbose_name = "SMILES Django Portal"
    url_prefix = "smiles"
    url_app_name = label
    url_home = url_app_name + ":home"
    fa_icon_class = "fa-circle"
    settings = Settings()
    nav = [
        {
            'label': 'Literature Data Products',
            'icon': 'fa fa-book',
            'url': 'smiles:lit-dp-list',
        },
        {
            'label': 'Computational Data Products',
            'icon': 'fa fa-database',
            'url': 'smiles:comp-dp-list',
        },
        {
            'label': 'Experimental Data Products',
            'icon': 'fa fa-flask',
            'url': 'smiles:exp-dp-list',
        },
        {
            'label': 'Upload Data Products',
            'icon': 'fa fa-upload',
            'url': 'smiles:upload-dps',
        },
    ]

    def ready(self):
        celery_app.autodiscover_tasks()

    def merge_settings(self, settings_module):
        WEBPACK_LOADER = getattr(settings_module, "WEBPACK_LOADER", {})
        WEBPACK_LOADER.update(Settings.WEBPACK_LOADER)
        settings_module.WEBPACK_LOADER = WEBPACK_LOADER
