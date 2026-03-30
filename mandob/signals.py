from mandob.models import MandobToken


def GenerateTokenMandob(sender, instance=None, created=False, **kwargs):
    if created:
        MandobToken.objects.create(user=instance)