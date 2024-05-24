from django.apps import AppConfig


import sys 
RUNNING_DEV_SERVER = 'runserver' in sys.argv

class BankdatasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bankDatas'

    def ready(self):
        if RUNNING_DEV_SERVER:
            from .tasks import scheduler
            scheduler.start()