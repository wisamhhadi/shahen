from django.apps import AppConfig
from django.db.models.signals import post_save


class MandobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mandob'

    def ready(self):
        from mandob.models import Mandob
        from mandob.signals import GenerateTokenMandob
        post_save.connect(GenerateTokenMandob, sender=Mandob)


