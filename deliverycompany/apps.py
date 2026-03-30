from django.apps import AppConfig
from django.db.models.signals import post_save


class DeliverycompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deliverycompany'

    def ready(self):
        from deliverycompany.models import DeliveryCompany
        from deliverycompany.signals import GenerateTokenDeliveryCompany
        from extra import GenerateBarcode

        post_save.connect(GenerateBarcode, sender=DeliveryCompany)
        post_save.connect(GenerateTokenDeliveryCompany, sender=DeliveryCompany)