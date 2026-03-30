from deliverycompany.models import DeliveryCompanyToken


def GenerateTokenDeliveryCompany(sender, instance=None, created=False, **kwargs):
    if created:
        DeliveryCompanyToken.objects.create(user=instance)
