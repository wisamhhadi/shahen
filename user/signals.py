from user.models import UserToken


def GenerateTokenUser(sender, instance=None, created=False, **kwargs):
    if created:
        UserToken.objects.create(user=instance)