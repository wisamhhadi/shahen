import binascii
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from extra import content_file_name, UserManager
from django.utils.translation import gettext_lazy as _
from shahen import settings


class DeliveryCompany(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_("الاسم"), max_length=200)
    phone = models.IntegerField(_("الهاتف"), unique=True)
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الدولة"), )
    province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("المحافظة"), )
    city = models.CharField(_("المدينة"), max_length=200)
    location = models.CharField(_("العنوان"), max_length=200)
    specialty = models.ForeignKey('core.Specialty', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name=_("التخصص"), )
    image = models.ImageField(_("الصورة"), upload_to=content_file_name, null=True, blank=True)

    id_doc1 = models.FileField(_("الهوية ١"), upload_to=content_file_name, null=True, blank=True)
    id_doc2 = models.FileField(_("الهوية ٢"), upload_to=content_file_name, null=True, blank=True)

    resident_doc1 = models.FileField(_("السكن ١"), upload_to=content_file_name, null=True, blank=True)
    resident_doc2 = models.FileField(_("السكن ٢"), upload_to=content_file_name, null=True, blank=True)

    company_registration = models.FileField(_("تسجيل الشركة"), upload_to=content_file_name, null=True, blank=True)
    company_doc1 = models.FileField(_("مرفق ١"), upload_to=content_file_name, null=True, blank=True)
    company_doc2 = models.FileField(_("مرفق ٢"), upload_to=content_file_name, null=True, blank=True)
    company_doc3 = models.FileField(_("مرفق ٣"), upload_to=content_file_name, null=True, blank=True)
    company_doc4 = models.FileField(_("مرفق ٤"), upload_to=content_file_name, null=True, blank=True)
    company_doc5 = models.FileField(_("مرفق ٥"), upload_to=content_file_name, null=True, blank=True)

    barcode = models.CharField(_("باركود"), max_length=200, null=True, blank=True)
    barcode_image = models.ImageField(_("صورة الباركود"), upload_to=content_file_name, null=True, blank=True)

    latitude_base = models.CharField(_("خط الطول للمنزل"), max_length=50, null=True, blank=True)
    longitude_base = models.CharField(_("خط العرض للمنزل"), max_length=50, null=True, blank=True)


    latitude = models.CharField(_("خط الطول"), max_length=50, null=True, blank=True)
    longitude = models.CharField(_("خط العرض"), max_length=50, null=True, blank=True)

    device_id = models.CharField(_("Device ID"), max_length=255, null=True, blank=True)

    balance = models.IntegerField(_("الرصيد"), default=0)
    pin = models.CharField(max_length=200, null=True, blank=True)
    is_logged = models.BooleanField(_("Is Logged"), default=False)


    id_number = models.CharField(_("رقم الهوية"), max_length=200,null=True, blank=True)
    id_issue_city = models.CharField(_("مكتب اصدار الهوية"), max_length=200, null=True, blank=True)
    id_issue_date = models.DateField(_("تاريخ الاصدار"), max_length=200, null=True, blank=True)
    id_expire_date = models.DateField(_("تاريخ النفاذ"), max_length=200, null=True, blank=True)
    id_birth_date = models.DateField(_("تاريخ الولادة"), max_length=200, null=True, blank=True)

    house_id_issuer = models.CharField(_("مكتب اصدار بطاقة السكن"), max_length=200, null=True, blank=True)
    house_id_house_number = models.CharField(_("رقم الدار"), max_length=200, null=True, blank=True)
    house_id_house_street = models.CharField(_("رقم الزقاق"), max_length=200, null=True, blank=True)
    house_id_house_city = models.CharField(_("رقم المحلة"), max_length=200, null=True, blank=True)

    employee = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

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


class DeliveryCompanyToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        DeliveryCompany, related_name='auth_token_delivery',
        on_delete=models.CASCADE, verbose_name=_("delivery")
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
