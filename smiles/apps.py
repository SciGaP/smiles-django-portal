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
    settings = Settings()

    # The following are Airavata Django Portal specific custom Django app settings

    # Set url_home to a namespaced URL that will be the homepage when the custom
    # app is selected from the main menu
    # url_home = "smiles:home"

    # Set fa_icon_class to a FontAwesome CSS class for an icon to associate with
    # the custom app. Find an icon class at https://fontawesome.com/icons?d=gallery&p=2&s=regular,solid&m=free
    fa_icon_class = "fa-circle"

    # Second level navigation. Defines sub-navigation that displays on the left
    # hand side navigation bar in the Django Portal. This is optional but
    # recommended if your custom Django app has multiple entry points. See the
    # description of *nav* in
    # https://apache-airavata-django-portal.readthedocs.io/en/latest/dev/new_django_app/#appconfig-settings
    # for more details for more details.

    def ready(self):
        celery_app.autodiscover_tasks()

    def merge_settings(self, settings_module):
        WEBPACK_LOADER = getattr(settings_module, "WEBPACK_LOADER", {})
        WEBPACK_LOADER.update(Settings.WEBPACK_LOADER)
        settings_module.WEBPACK_LOADER = WEBPACK_LOADER
