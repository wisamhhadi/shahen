import random
import datetime
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from django.core.files import File
from django.db import IntegrityError
from django.contrib.auth.base_user import BaseUserManager


def user_content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "user/%s_%s_%s.%s" % (
    random.randint(0, 999999999), datetime.datetime.now().day, datetime.datetime.now().second, ext)
    return filename


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "uploads/%s_%s_%s.%s" % (
    random.randint(0, 999999999), datetime.datetime.now().day, datetime.datetime.now().second, ext)
    return filename


def barcode_content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "barcode/%s_%s_%s.%s" % (
    random.randint(0, 999999999), datetime.datetime.now().day, datetime.datetime.now().second, ext)
    return filename


def GenerateBarcode(sender, instance, **kwargs):
    if not instance.barcode and instance.barcode is None:
        while True:
            try:
                code, buffer = CreateBarcode()
                instance.barcode = code
                instance.barcode_image.save('%s' % code + '.png', File(buffer), save=False)
                instance.save()
                break
            except IntegrityError:
                pass


def CreateBarcode():
    code = random.randint(1111111111111, 8888888888888)
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN('%s' % code, writer=ImageWriter())
    buffer = BytesIO()
    ean.write(buffer)
    return ean.ean, buffer


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone)
        user.set_password(password)
        # for field , value in extra_fields.items():
        #     if hasattr(user,field) and field != 'groups' and field != 'user_permissions':
        #         setattr(user,field,value)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)
