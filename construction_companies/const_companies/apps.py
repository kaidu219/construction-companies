import os
from django.apps import AppConfig
from django.conf import settings

from .utils import insert_data_file


class ConstCompaniesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'const_companies'

    def ready(self) -> None:
        ctx = super().ready()
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'storage.json')):
            insert_data_file()
        return ctx