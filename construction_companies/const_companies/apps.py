import os
from django.apps import AppConfig
from django.conf import settings

from .utils import insert_data_file

import schedule
import time

class ConstCompaniesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'const_companies'

    def ready(self) -> None:
        ctx = super().ready()
        

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'storage.json')):
            insert_data_file()
        
        # schedule.every(3600).seconds.do(insert_data_file)
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)

        return ctx
    
  
