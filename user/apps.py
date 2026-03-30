from django.apps import AppConfig
from django.db.models.signals import post_save


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from user.models import User
        from user.signals import GenerateTokenUser
        from extra import GenerateBarcode

        post_save.connect(GenerateBarcode, sender=User)
        post_save.connect(GenerateTokenUser, sender=User)
