import binascii
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from extra import content_file_name, UserManager
from django.utils.translation import gettext_lazy as _
from shahen import settings

CLIENT_TYPE = (
    ("user", "زبون"),
    ("company", "تاجر"),
)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_("الاسم"), max_length=200)
    phone = models.IntegerField(_("الهاتف"), unique=True)
    language = models.ForeignKey('core.Language', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("اللغة"), )
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الدولة"), )
    province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("المحافظة"), )
    activity_type = models.ForeignKey('core.ActivityType', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name=_("نوع النشاط"))
    city = models.CharField(_("المدينة"), max_length=200)
    location = models.CharField(_("العنوان"), max_length=200)
    max_debt = models.IntegerField(_("الحد الاقصى للدين"), default=0)

    image = models.ImageField(_("الصورة"), upload_to=content_file_name, null=True, blank=True)
    id_doc1 = models.FileField(_("الهوية 1"), upload_to=content_file_name, null=True, blank=True)
    id_doc2 = models.FileField(_("الهوية 2"), upload_to=content_file_name, null=True, blank=True)

    barcode = models.CharField(_("باركود"), max_length=200, null=True, blank=True)
    barcode_image = models.ImageField(_("صورة الباركود"), upload_to=content_file_name, null=True, blank=True)
    latitude = models.CharField(_("خط الطول"), max_length=50, null=True, blank=True)
    longitude = models.CharField(_("خط العرض"), max_length=50, null=True, blank=True)

    latitude_base = models.CharField(_("خط الطول للمنزل"), max_length=50, null=True, blank=True)
    longitude_base = models.CharField(_("خط العرض للمنزل"), max_length=50, null=True, blank=True)

    device_id = models.CharField(_("Device ID"), max_length=255, null=True, blank=True)

    type = models.CharField(_("نوع الزبون"), max_length=200, default="user", choices=CLIENT_TYPE)

    company_name = models.CharField(_("اسم الشركة"), max_length=200, null=True, blank=True)
    company_doc = models.FileField(_("شهادة تآسيس الشركة"), upload_to=content_file_name, null=True, blank=True)
    pin = models.CharField(max_length=200, null=True, blank=True)

    id_number = models.CharField(_("رقم الهوية"), max_length=200, null=True, blank=True)
    id_issue_city = models.CharField(_("مكتب اصدار الهوية"), max_length=200, null=True, blank=True)
    id_issue_date = models.DateField(_("تاريخ الاصدار"), max_length=200, null=True, blank=True)
    id_expire_date = models.DateField(_("تاريخ النفاذ"), max_length=200, null=True, blank=True)
    id_birth_date = models.DateField(_("تاريخ الولادة"), max_length=200, null=True, blank=True)

    house_id_issuer = models.CharField(_("مكتب اصدار بطاقة السكن"), max_length=200, null=True, blank=True)
    house_id_house_number = models.CharField(_("رقم الدار"), max_length=200, null=True, blank=True)
    house_id_house_street = models.CharField(_("رقم الزقاق"), max_length=200, null=True, blank=True)
    house_id_house_city = models.CharField(_("رقم المحلة"), max_length=200, null=True, blank=True)

    employee = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("الموظف"), )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
    is_logged = models.BooleanField(_("Is Logged"), default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    user_permissions = None
    groups = None
    first_name = None
    last_name = None

    objects = UserManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        default_permissions = ()


class UserToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        User, related_name='auth_token_user',
        on_delete=models.CASCADE, verbose_name=_("user")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("seller Token")
        verbose_name_plural = _("sellers Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class UserRoom(models.Model):
    room = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class UserMessage(models.Model):
    room = models.ForeignKey(UserRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
