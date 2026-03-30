import binascii
import os
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from extra import content_file_name, UserManager, user_content_file_name
from django.utils.translation import gettext_lazy as _

from shahen import settings

STATUS = (
    ("pending", "قيد المراجعة"),
    ("accepted", "مقبول"),
)


class Mandob(AbstractBaseUser, PermissionsMixin):
    admin = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="mandob_owner",
                              verbose_name=_("المسؤول"))
    phone = models.BigIntegerField(_("الهاتف"), unique=True)
    name = models.CharField(_("الاسم"), max_length=200)
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الدولة"), )
    province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("المحافظة"), )
    city = models.CharField(_("المدينة"), max_length=200,null=True, blank=True)
    location = models.CharField(_("العنوان"), max_length=200,null=True, blank=True)

    app_language = models.ForeignKey('core.Language', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("لغة التطبيق"))
    registration_fee = models.IntegerField(_("اجور التسجيل"), default=0)
    salary = models.IntegerField(_("الراتب"), default=0)
    note = models.TextField(_("ملاحظات"), blank=True, null=True)

    shift_start = models.TimeField(_("اوقات العمل ( من )"), blank=True, null=True)
    shift_stop = models.TimeField(_("اوقات العمل ( الى )"), blank=True, null=True)
    late_hour = models.IntegerField(_("سماحية التآخير"),default=0)
    late_cost = models.IntegerField(_("غرامة التآخير على كل ساعة"),default=0)

    latitude = models.CharField(_("خط الطول"), max_length=50, null=True, blank=True)
    longitude = models.CharField(_("خط العرض"), max_length=50, null=True, blank=True)
    radius = models.IntegerField(_("نصف القطر ( بالامتار )"), default=0, null=True, blank=True)

    image = models.ImageField(upload_to=user_content_file_name, blank=True, null=True, verbose_name=_("الصورة"))

    id_doc1 = models.ImageField(_("الهوية ١"), upload_to=content_file_name, null=True, blank=True)
    id_doc2 = models.ImageField(_("الهوية ٢"), upload_to=content_file_name, null=True, blank=True)

    resident_doc1 = models.ImageField(_("بطاقة السكن ١"), upload_to=content_file_name, null=True, blank=True)
    resident_doc2 = models.ImageField(_("بطاقة السكن ٢"), upload_to=content_file_name, null=True, blank=True)

    attachment1 = models.ImageField(_("مرفق ١"), upload_to=content_file_name, null=True, blank=True)
    attachment2 = models.ImageField(_("مرفق ٢"), upload_to=content_file_name, null=True, blank=True)

    status = models.CharField(_("حالة المندوب"), max_length=200, default="pending", choices=STATUS)

    balance = models.IntegerField(_("الرصيد"), default=0)
    pin = models.CharField(max_length=200, null=True, blank=True)

    latitude_base = models.CharField(_("خط الطول للمنزل"), max_length=50, null=True, blank=True)
    longitude_base = models.CharField(_("خط العرض للمنزل"), max_length=50, null=True, blank=True)

    latitude2 = models.CharField(_("خط الطول الحالي"), max_length=50, null=True, blank=True)
    longitude2 = models.CharField(_("خط العرض الحالي"), max_length=50, null=True, blank=True)

    captain_goal = models.IntegerField(_("هدف السائقين"), default=0, null=True, blank=True)
    user_goal = models.IntegerField(_("هدف الزبائن"), default=0, null=True, blank=True)
    company_goal = models.IntegerField(_("هدف الشركات"), default=0, null=True, blank=True)
    delivery_company_goal = models.IntegerField(_("هدف الناقلين"), default=0, null=True, blank=True)
    car_goal = models.IntegerField(_("هدف المركبات"), default=0, null=True, blank=True)

    id_number = models.CharField(_("رقم الهوية"), max_length=200,null=True, blank=True)
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
    is_free = models.BooleanField(_("عمل خارجي"), default=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    updatedtime = models.TimeField(_("وقت اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    user_permissions = None
    groups = None
    first_name = None
    last_name = None
    is_logged = models.BooleanField(_("Is Logged"), default=False)
    device_id = models.CharField(_("Device ID"), max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return str(self.name)


class Attendance(models.Model):
    mandob = models.ForeignKey(Mandob, on_delete=models.CASCADE, verbose_name=_("المندوب"))
    day = models.DateField(_("اليوم"), )
    attend_time = models.TimeField(_("تاريخ البدآ"), )
    leave_time = models.TimeField(_("تاريخ الانتهاء"), )
    work_hour = models.IntegerField(_("وقت العمل"), default=0)
    late_hour = models.IntegerField(_("وقت التأخير"), default=0)

    employee = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("الموظف"), )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.mandob.name)


class MandobToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        Mandob, related_name='auth_token_mandob',
        on_delete=models.CASCADE, verbose_name=_("mandob")
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


TYPES = (
    ("day", "يومي"),
    ("week", "اسبوعي"),
    ("month", "شهري"),
    ("year", "سنوي"),
)

ANSWER_TYPES = (
    ("text", "نصي"),
    ("bool", "نعم/كلا"),
    ("choice", "اختيار متعدد"),
)

TARGET_TYPES = (
    ("mandob", "المندوبين"),
    ("captain", "السائقين"),
    ("company", "الناقلين"),
)


class CustomReport(models.Model):
    mandob = models.ForeignKey(Mandob, on_delete=models.CASCADE, verbose_name=_("المندوب"), null=True, blank=True)
    target_type = models.CharField(_("الفئة المستهدفة"), max_length=200, choices=TARGET_TYPES)
    title = models.CharField(_("عنوان التقرير"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Question(models.Model):
    custom_report = models.ForeignKey(CustomReport, on_delete=models.CASCADE, null=True, blank=True)
    type = models.TextField(_("نوع التقرير"), max_length=200, choices=TYPES,default="day")
    title = models.TextField(_("السؤال"))
    answer_type = models.CharField(_("نوع السؤال"), max_length=200, choices=ANSWER_TYPES, default="text")
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name=_("السؤال"))
    choice_text = models.CharField(_("نص الخيار"), max_length=500)
    order = models.PositiveIntegerField(_("ترتيب الخيار"), default=0)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    class Meta:
        verbose_name = _("خيار السؤال")
        verbose_name_plural = _("خيارات الأسئلة")
        ordering = ['order', 'created']
        unique_together = ['question', 'choice_text']

    def __str__(self):
        return f"{self.question.title[:30]}... - {self.choice_text}"


class CustomAnswer(models.Model):
    custom_report = models.ForeignKey(CustomReport, on_delete=models.CASCADE, verbose_name=_("الاستبيان"))
    mandob = models.ForeignKey(Mandob, on_delete=models.CASCADE, verbose_name=_("المندوب"))
    question = models.CharField(verbose_name=_("السؤال"),max_length=200)
    answer_type = models.CharField(_("نوع السؤال"), max_length=200, choices=ANSWER_TYPES, default="text")
    answer = models.TextField(_("جواب"))
    note = models.TextField(_("ملاحظات"), blank=True, null=True)
    file1 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file2 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file3 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file4 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file5 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Report(models.Model):
    mandob = models.ForeignKey(Mandob, on_delete=models.CASCADE, verbose_name=_("المندوب"))
    type = models.CharField(_("نوع الاستبيان"), max_length=200, choices=TYPES, default="day")
    latitude = models.CharField(_("خط الطول"), max_length=50, null=True, blank=True)
    longitude = models.CharField(_("خط العرض"), max_length=50, null=True, blank=True)
    file1 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file2 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file3 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file4 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file5 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Answer(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name=_("الاستبيان"))
    question = models.CharField(verbose_name=_("السؤال"),max_length=200)
    answer_type = models.CharField(_("نوع السؤال"), max_length=200, choices=ANSWER_TYPES, default="text")
    answer = models.TextField(_("جواب"))
    note = models.TextField(_("ملاحظات"), blank=True, null=True)
    file1 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file2 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file3 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file4 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file5 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


REGISTER_TYPES = (
    ("captain", "سائق"),
    ("user", "زبون"),
    ("company", "تاجر"),
    ("deliverycompany", "ناقل"),
    ("car", "سيارة"),
)


class History(models.Model):
    mandob = models.ForeignKey(Mandob, on_delete=models.CASCADE, verbose_name=_("المندوب"))
    type = models.CharField(_("النوع"), choices=REGISTER_TYPES, max_length=200)
    barcode = models.CharField(_("الباركو"), max_length=200, unique=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


CURRENCY_CHOICES = (
    ("iqd", "دينار"),
    ("usd", "دولار"),
    ("euro", "يورو"),
)

PAY_CHOICES = (
    ("now", "نقد"),
    ("later", "اجل")
)


class OrderReport(models.Model):
    mandob = models.ForeignKey(Mandob, on_delete=models.CASCADE, verbose_name=_("المندوب"))
    name = models.CharField(_("الاسم"), max_length=200)
    location = models.CharField(_("العنوان"), max_length=200)
    currency = models.CharField(_("العملة"), max_length=200, choices=CURRENCY_CHOICES, default="iqd")
    type = models.CharField(_("النوع"), max_length=200, choices=PAY_CHOICES, default="now")
    paid = models.IntegerField(_("المدفوع"), default=0)
    last = models.IntegerField(_("المتبقي"), default=0)
    total_price = models.IntegerField(_("السعر الكلي"), default=0)
    note = models.TextField(_("ملاحظات"), blank=True, null=True)
    file1 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file2 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file3 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file4 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file5 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    latitude = models.CharField(_("خط الطول"), max_length=50, null=True, blank=True)
    longitude = models.CharField(_("خط العرض"), max_length=50, null=True, blank=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


ITEM_TYPE = (
    ("sell", "بيع"),
    ("buy", "شراء"),
    ("maintain", "صيانة"),
    ("service", "خدمة"),
)


class OrderReportItem(models.Model):
    order = models.ForeignKey(OrderReport, on_delete=models.CASCADE)
    name = models.CharField(_("الاسم"), max_length=200)
    category = models.CharField(_("الصنف"), max_length=200)
    type = models.CharField(_("النوع"), choices=ITEM_TYPE, max_length=200, default="sell")
    count = models.IntegerField(_("العدد"), default=1)
    file1 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file2 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file3 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file4 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    file5 = models.FileField(_("مرفقات"), upload_to=content_file_name, null=True, blank=True)
    price = models.IntegerField(_("السعر"), default=0)
    total_price = models.IntegerField(_("السعر الكلي"), default=0)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Room(models.Model):
    room = models.ForeignKey(Mandob, on_delete=models.CASCADE)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    mandob = models.ForeignKey(Mandob, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
