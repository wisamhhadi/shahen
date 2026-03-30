import binascii
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from extra import content_file_name , UserManager
from django.utils.translation import gettext_lazy as _

from shahen import settings

STATUS = (
    ("pending", "قيد المراجعة"),
    ("accepted", "مقبول"),
)


class Captain(AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    car = models.ForeignKey('core.Car', on_delete=models.SET_NULL, null=True, blank=True, related_name="car_captain_model",
                            verbose_name=_("السيارة"))
    name = models.CharField(_("الاسم"), max_length=200)
    phone = models.IntegerField(_("الهاتف"), unique=True)
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الدولة"))
    province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("المحافظة"))
    city = models.CharField(_("المدينة"), max_length=200,null=True, blank=True)
    location = models.CharField(_("العنوان"), max_length=200,null=True, blank=True)
    languages = models.ManyToManyField('core.Language', verbose_name=_("اللغات"),null=True, blank=True)
    app_language = models.ForeignKey('core.Language', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='app_language', verbose_name=_("لغة التطبيق"))
    note = models.TextField(_("ملاحظات"), blank=True, null=True)

    image = models.ImageField(_("الصورة"), upload_to=content_file_name, blank=True, null=True)

    personal_id_doc1 = models.FileField(_("الهوية ١"), upload_to=content_file_name, blank=True, null=True)
    personal_id_doc2 = models.FileField(_("الهوية ٢"), upload_to=content_file_name, blank=True, null=True)

    car_id_doc1 = models.FileField(_("السنوية ١"), upload_to=content_file_name, blank=True, null=True)
    car_id_doc2 = models.FileField(_("السنوية ١"), upload_to=content_file_name, blank=True, null=True)

    agency_doc = models.FileField(_("الوكالة"), upload_to=content_file_name, blank=True, null=True)

    resident_doc1 = models.FileField(_("السكن ١"), upload_to=content_file_name, blank=True, null=True)
    resident_doc2 = models.FileField(_("السكن ٢"), upload_to=content_file_name, blank=True, null=True)

    barcode = models.CharField(_("الباركود"), max_length=200, null=True, blank=True)
    barcode_image = models.ImageField(_("صورة الباركود"), upload_to=content_file_name, blank=True, null=True)

    latitude_base = models.CharField(_("خط الطول للمنزل"), max_length=50, null=True, blank=True)
    longitude_base = models.CharField(_("خط العرض للمنزل"), max_length=50, null=True, blank=True)

    latitude = models.CharField(_("خط الطول"), max_length=50, null=True, blank=True)
    longitude = models.CharField(_("خط العرض"), max_length=50, null=True, blank=True)

    status = models.CharField(_("الحالة"), max_length=50, default="pending", choices=STATUS)
    pin = models.CharField(max_length=200, null=True, blank=True)
    device_id = models.CharField(_("Device ID"), max_length=255, null=True, blank=True)
    is_logged = models.BooleanField(_("Is Logged"), default=False)

    # documents details
    id_number = models.CharField(_("رقم الهوية"), max_length=200,null=True, blank=True)
    id_issue_city = models.CharField(_("مكتب اصدار الهوية"), max_length=200, null=True, blank=True)
    id_issue_date = models.DateField(_("تاريخ الاصدار"), max_length=200, null=True, blank=True)
    id_expire_date = models.DateField(_("تاريخ النفاذ"), max_length=200, null=True, blank=True)
    id_birth_date = models.DateField(_("تاريخ الولادة"), max_length=200, null=True, blank=True)

    house_id_issuer = models.CharField(_("مكتب اصدار بطاقة السكن"), max_length=200, null=True, blank=True)
    house_id_house_number = models.CharField(_("رقم الدار"), max_length=200, null=True, blank=True)
    house_id_house_street = models.CharField(_("رقم الزقاق"), max_length=200, null=True, blank=True)
    house_id_house_city = models.CharField(_("رقم المحلة"), max_length=200, null=True, blank=True)

    driving_id_expire = models.CharField(_("تاريخ نفاذ اجازة القيادة"), max_length=200, null=True, blank=True)

    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    updatedtime = models.TimeField(_("وقت اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    user_permissions = None
    groups = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        default_permissions = ()


class CaptainToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        Captain, related_name='auth_token_captain',
        on_delete=models.CASCADE, verbose_name=_("captain")
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


class CaptainRoom(models.Model):
    room = models.ForeignKey(Captain, on_delete=models.CASCADE)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class CaptainMessage(models.Model):
    room = models.ForeignKey(CaptainRoom, on_delete=models.CASCADE)
    captain = models.ForeignKey(Captain, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
