from django.apps import AppConfig
from django.db.models.signals import post_save


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .models import Car
        from extra import GenerateBarcode

        post_save.connect(GenerateBarcode, sender=Car)
