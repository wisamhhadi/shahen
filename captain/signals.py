from captain.models import CaptainToken


def GenerateTokenCaptain(sender, instance=None, created=False, **kwargs):
    if created:
        CaptainToken.objects.create(user=instance)