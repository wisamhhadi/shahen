from django.apps import AppConfig
from django.db.models.signals import post_save


class CaptainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'captain'

    def ready(self):
        from captain.models import Captain
        from captain.signals import GenerateTokenCaptain
        from extra import GenerateBarcode

        post_save.connect(GenerateBarcode, sender=Captain)
        post_save.connect(GenerateTokenCaptain, sender=Captain)
