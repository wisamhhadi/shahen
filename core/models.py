from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
# from simple_history.models import HistoricalRecords
from extra import user_content_file_name, content_file_name, UserManager

USER_TYPE = (
    ('client1', 'زبون عادي'),
    ('client2', 'زبون تاجر'),
    ('captain', 'سائق'),
    ('deliveryCompany', 'شركة نقل'),
    ('mandob', 'مندوب'),
    ('admin', 'لوحة تحكم'),
)

CLIENT_TYPE = (
    ("user", "زبون"),
    ("company", "تاجر"),
)

PAY_TYPE = (
    ("get", "قبض"),
    ("pay", "دفع"),
)


class Country(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الدولة"))
    name = models.CharField(_("الاسم"), max_length=200)
    from_prec = models.FloatField(_("النسبة من"), default=0)
    to_prec = models.FloatField(_("النسبة الى"), default=0)
    inner_ride_start_price = models.IntegerField(_("سعر بداية الرحلة الداخلي"), default=0)
    outer_ride_start_price = models.IntegerField(_("سعر بداية الرحلة الخارجي"), default=0)
    company_prec = models.FloatField(_("نسبة الشركة"), default=0)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(f"{self.name}")


class Permission(models.Model):
    name = models.CharField(_("الاسم"), max_length=50)
    model_name = models.CharField(_("اسم المودل"), max_length=100)
    create = models.BooleanField(_("انشاء"), default=False)
    update = models.BooleanField(_("تعديل"), default=False)
    list = models.BooleanField(_("عرض"), default=False)
    delete = models.BooleanField(_("حذف"), default=False)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class PermissionGroup(models.Model):
    name = models.CharField(_("اسم الكروب"), max_length=50)
    permission = models.ManyToManyField(Permission, verbose_name=_("الصلاحيات"))
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Admin(AbstractBaseUser, PermissionsMixin):
    phone = models.BigIntegerField(_('الهاتف'), unique=True)
    name = models.CharField(_("الاسم"), max_length=200)
    job_title = models.CharField(_("المسمى الوظيفي"), max_length=200)
    salary = models.IntegerField(_("الراتب"), default=0)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_manager',
                                verbose_name=_("المسؤول"))
    image = models.ImageField(_("الصورة"), upload_to=user_content_file_name, null=True, blank=True)
    permission_group = models.ForeignKey(PermissionGroup, on_delete=models.SET_NULL, null=True, blank=True,
                                         verbose_name=_("الصلاحيات"), )

    is_active = models.BooleanField(_("فعال؟"), default=True)
    is_staff = models.BooleanField(_("مسؤول مندوبين ؟"), default=False)
    employee = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
    note = models.TextField(_("ملاحظات"), blank=True)

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


class Language(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Specialty(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CarCompany(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CarModel(models.Model):
    car_company = models.ForeignKey(CarCompany, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name=_("شركة السيارة"))
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CarColor(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CarCategory(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class GoodsType(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CarSize(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    max_load = models.CharField(_("اقصى حمل"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Trailer(models.Model):
    car_category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("فئة السيارة"), )
    goods_type = models.ManyToManyField(GoodsType, verbose_name=_("نوع الحمولة"), related_name="goods_types")
    car_size = models.ForeignKey(CarSize, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("حجم السيارة"))
    name = models.CharField(_("الاسم"), max_length=200)

    km_price = models.IntegerField(_("سعر الكيلو متر"), default=0)
    worker_prec = models.FloatField(_("نسبة عامل تخصص"), default=0)
    weight_prec = models.FloatField(_("نسبة عامل الوزن"), default=0)
    company_prec = models.FloatField(_("نسبة الشركة"), default=0)
    can_order_workers = models.BooleanField(_("هل يمكنه طلب عمال"), default=False)
    car_hour_price = models.IntegerField(_("سعر ساعة عمل الالية"), default=0)
    worker_hour_price = models.IntegerField(_("سعر ساعة عامل"), default=0)
    inner_ride_start_price = models.IntegerField(_("سعر بداية الرحلة الداخلي"), default=0)
    outer_ride_start_price = models.IntegerField(_("سعر بداية الرحلة الخارجي"), default=0)

    captain_prize = models.IntegerField(_("مكافئة السائق"), default=0)
    mandob_prize = models.IntegerField(_("مكافئة المندوب"), default=0)

    late_loading_price = models.IntegerField(_("غرامة التاخير بالتحميل"), default=0)
    late_loading_days = models.IntegerField(_("عدد ايام التاخير بالتحميل"), default=0)
    late_delivering_price = models.IntegerField(_("غرامة التاخير بالتفريغ"), default=0)
    late_delivering_days = models.IntegerField(_("عدد ايام التاخير بالتفريغ"), default=0)

    image1 = models.ImageField(_("صورة القاطرة ١"), upload_to=content_file_name, null=True, blank=True)
    image2 = models.ImageField(_("صورة القاطرة ٢"), upload_to=content_file_name, null=True, blank=True)
    image3 = models.ImageField(_("صورة القاطرة ٣"), upload_to=content_file_name, null=True, blank=True)
    map_icon = models.ImageField(_("ايقونة الخريطة"), upload_to=content_file_name, null=True, blank=True)
    order_icon = models.ImageField(_("ايقونة الطلب"), upload_to=content_file_name, null=True, blank=True)

    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CarLetter(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class ActivityType(models.Model):
    name = models.CharField(_("الاسم"), max_length=200)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Car(models.Model):
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='car_model_captain', verbose_name=_("السائق"))
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="car_model_company", verbose_name=_("الشركة"))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الدولة"))
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))
    car_number = models.CharField(_("رقم السيارة"), max_length=200)
    car_letter = models.ForeignKey(CarLetter, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name=_("حرف السيارة"))
    car_category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("فئة السيارة"))
    trailer = models.ForeignKey(Trailer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("القاطرة"))
    car_company = models.ForeignKey(CarCompany, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name=_("شركة السيارة"))
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name=_("موديل السيارة"))
    car_color = models.ForeignKey(CarColor, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name=_("لون السيارة"))

    car_manu_year = models.IntegerField(_("سنة التصنيع"), default=0)
    car_doc1 = models.FileField(_("السنوية ١"), upload_to=content_file_name, null=True, blank=True)
    car_doc2 = models.FileField(_("السنوية ٢"), upload_to=content_file_name, null=True, blank=True)
    image1 = models.ImageField(_("مرفق ١"), upload_to=content_file_name, null=True, blank=True)
    image2 = models.ImageField(_("مرفق ٢"), upload_to=content_file_name, null=True, blank=True)
    image3 = models.ImageField(_("مرفق ٣"), upload_to=content_file_name, null=True, blank=True)

    agency_doc = models.FileField(_("الوكالة"), upload_to=content_file_name, blank=True, null=True)

    car_id_name = models.CharField(_("اسم صاحب السنوية"), max_length=200, null=True, blank=True)
    car_id_number = models.CharField(_("رقم السنوية"), max_length=200, null=True, blank=True)
    car_id_vin = models.CharField(_("رقم الشاصي"), max_length=200, null=True, blank=True)
    car_id_expire = models.DateField(_('تاريخ نفاذ السنوية'), blank=True, null=True)

    barcode = models.CharField(_("باركود"), max_length=200, null=True, blank=True)
    barcode_image = models.ImageField(_("صورة الباركود"), upload_to=content_file_name, null=True, blank=True)

    balance = models.IntegerField(_("الرصيد"), default=0)
    max_balance = models.IntegerField(_("الحد الاقصى للرصيد"), default=0)

    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)

    def __str__(self):
        return str(self.car_number)


class Pay(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المستخدم"))
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    mandob = models.ForeignKey('mandob.Mandob', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_("المندوب"))
    user_type = models.CharField(_("نوع المستخدم"), max_length=200, default="mandob", choices=USER_TYPE)
    pay_type = models.CharField(_("نوع السند"), max_length=200, choices=PAY_TYPE, default="get")
    amount = models.IntegerField(_("القيمة"), default=0, )
    note = models.TextField(_("ملاحظات"), blank=True, null=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class PrePaid(models.Model):
    user_type = models.CharField(max_length=200, default="mandob", choices=USER_TYPE, verbose_name=_("نوع المستخدم"))

    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الزبون"))
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    mandob = models.ForeignKey('mandob.Mandob', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_("المندوب"))

    code = models.CharField(_("الكود"), max_length=200)
    amount = models.IntegerField(_("القيمة"), default=0, )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Fine(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المستخدم"))
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    mandob = models.ForeignKey('mandob.Mandob', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_("المندوب"))
    user_type = models.CharField(_("نوع المستخدم"), max_length=200, default="mandob", choices=USER_TYPE)
    amount = models.IntegerField(_("القيمة"), default=0, )
    note = models.TextField(_("ملاحظات"), blank=True, null=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Notification(models.Model):
    user_type = models.CharField(_("نوع المستخدم"), max_length=200, choices=USER_TYPE)

    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الزبون"))
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    mandob = models.ForeignKey('mandob.Mandob', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_("المندوب"))

    title = models.CharField(_("العنوان"), max_length=200)
    text = models.TextField(_("النص"), null=True, blank=True)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Banner(models.Model):
    image = models.ImageField(_("الصورة"), upload_to=content_file_name)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Blog(models.Model):
    title = models.CharField(_('العنوان'), max_length=200)
    body = models.TextField(_('المحتوى'))
    image = models.ImageField(_("الصورة"), upload_to=content_file_name)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class Info(models.Model):
    whatsapp = models.CharField(_("واتس اب"), null=True, blank=True, max_length=200)
    facebook = models.CharField(_("فيسبوك"), null=True, blank=True, max_length=200)
    instagram = models.CharField(_("انستغرام"), null=True, blank=True, max_length=200)
    tiktok = models.CharField(_("تيك توك"), null=True, blank=True, max_length=200)
    about = models.CharField(_("عنا"), null=True, blank=True, max_length=200)
    privacy = models.CharField(_("الخصوصية"), null=True, blank=True, max_length=200)
    offer_time = models.IntegerField(_('وقت العرض'), default=0, null=True, blank=True)
    employee = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الموظف"), )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


LINKS = (
    ("الرئيسية", "/"),
    ("الموظفين", "/list_admin"),
    ("الناقلين", "/list_delivery_company"),
    ("السائقين", "/list_captain"),
    ("الزبائن", "/list_user"),
    ("المندوبين", "/list_mandob"),
    ("التقارير الاستبيانية", "/list_custom_reports"),
    ("التقارير الدورية", "/list_report"),
    ("تقارير الفواتير", "/list_order_report"),
    ("الاسئلة اليومية", "/day_mandob_question_view"),
    ("الاسئلة الاسبوعية", "/week_mandob_question_view"),
    ("الاسئلة الشهرية", "/month_mandob_question_view"),
    ("الاسئلة السنوية", "/year_mandob_question_view"),
    ("الشحنات", "/list_order"),
    ("المركبات", "/list_car"),
    ("سحب وايداع الرصيد", "/list_pay"),
    ("اكواد الرصيد", "/list_pre_paid"),
    ("الغرامات", "/list_fine"),
    ("الدول", "/country_view"),
    ("المحافظات", "/list_province"),
    ("التخصصات", "/specialty_view"),
    ("اللغات", "/language_view"),
    ("الانشطة", "/activity_type_view"),
    ("انواع الحمولة", "/goods_type_view"),
    ("شركات السيارات", "/car_company_view"),
    ("الوان السيارات", "/car_color_view"),
    ("احرف السيارات", "/car_letter_view"),
    ("فئات السيارات", "/car_category_view"),
    ("انواع المقطورات", "/list_trailer"),
    ("موديلات السيارات", "/car_model_view"),
    ("احجام السيارات", "/car_size_view"),
    ("بنرات التطبيق", "/banner_view"),
    ("المدونة", "/blog_view"),
    ("اشعارات", "/list_notification"),
    ("اعدادات", "/update_info/1"),
    ("فوائم", ""),
)


class Menu(models.Model):
    name = models.CharField(_(""), max_length=200)
    is_active = models.BooleanField(_(""), default=True)
    created = models.DateTimeField(auto_now_add=True)


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, )
    name = models.CharField(_(""), max_length=200)
    link = models.CharField(_(""), max_length=200)
    icon = models.CharField(_(""), max_length=200)
    order = models.IntegerField(_(""), default=0)
    is_active = models.BooleanField(_(""), default=True)
    created = models.DateTimeField(auto_now_add=True)
