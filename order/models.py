from django.db import models
from django.utils.translation import gettext_lazy as _
# from simple_history.models import HistoricalRecords
from extra import content_file_name

ORDER_TYPE = (
    ("internal", "داخلي"),
    ("external", "خارجي"),
)

# D=]$3R426!8F486A
class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المستخدم "))
    collection_area = models.CharField(_("نقطة التجمع"), max_length=200)
    collection_area_details = models.TextField(_("تفاصبل نقطة التجمع"), blank=True, null=True, )
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    rejection_reason = models.CharField(_("سبب الالغاء"), max_length=200)

    loading_workers_count = models.IntegerField(_("عدد عمال التحميل"), default=0)
    loading_workers_cost = models.IntegerField(_("سعر عمال التحميل"), default=0)

    delivering_workers_count = models.IntegerField(_("عدد عمال التفريغ"), default=0)
    delivering_workers_cost = models.IntegerField(_("سعر عمال التفريغ"), default=0)

    distance = models.CharField(_("المسافة"), max_length=10, default=0)

    order_type = models.CharField(_("نوع الرحلة"), max_length=200, choices=ORDER_TYPE)
    captain_status = models.CharField(_("حالة السائق"), max_length=200)
    client_status = models.CharField(_("حالة الزبون"), max_length=200)

    manifest = models.FileField(_("صورة المنفست"), upload_to=content_file_name, blank=True, null=True)
    captain_doc = models.FileField(_("صورة تعهد السائق"), upload_to=content_file_name, blank=True, null=True)
    client_doc = models.FileField(_("صورة تعهد المستخدم"), upload_to=content_file_name, blank=True, null=True)

    note = models.TextField(_("ملاحظات"), blank=True, null=True)
    client_rating = models.IntegerField(_("تقييم المستخدم"), default=0)
    captain_rating = models.IntegerField(_("تقييم السائق"), default=0)

    is_active = models.BooleanField(_("فعال؟"), default=True)
    employee = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("الموظف"), )
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class OrderCar(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الشحنة"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    car = models.ForeignKey('core.Car', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("السيارة"))
    trailer = models.ForeignKey('core.Trailer', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("المقطورة"))
    trailer_count = models.IntegerField(_("عدد المقطورات"), default=0)

    goods_cost = models.IntegerField(_("قيمة البضاعة"), default=0)
    goods_count = models.IntegerField(_("عدد البضاعة"), default=0)
    goods_details = models.TextField(_("وصف البضاعة"), blank=True, null=True, )
    goods_type = models.ForeignKey('core.GoodsType', on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name=_("نوع البضاعة"))

    before_loading_image1 = models.ImageField(_("صورة قبل التحميل ١"), upload_to=content_file_name, null=True,
                                              blank=True)
    before_loading_image2 = models.ImageField(_("صورة قبل التحميل ٢"), upload_to=content_file_name, null=True,
                                              blank=True)
    before_loading_image3 = models.ImageField(_("صورة قبل التحميل ٣"), upload_to=content_file_name, null=True,
                                              blank=True)

    after_delivering_image1 = models.ImageField(_("صورة بعد التفريغ ١"), upload_to=content_file_name, null=True,
                                                blank=True)
    after_delivering_image2 = models.ImageField(_("صورة بعد التفريغ ٢"), upload_to=content_file_name, null=True,
                                                blank=True)
    after_delivering_image3 = models.ImageField(_("صورة بعد التفريغ ٣"), upload_to=content_file_name, null=True,
                                                blank=True)

    note = models.TextField(_("ملاحظات"), blank=True, null=True)

    delivery_date = models.DateField(_("تاريخ الشحن"),)
    delivery_time = models.TimeField(_("وقت الشحن"), )

    from_country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="from_country", verbose_name=_("من الدولة"))
    from_province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="from_province", verbose_name=_("من المحافظة"))
    from_name = models.CharField(_("من الاسم"), max_length=200)
    from_lat = models.CharField(_("من خط الطول"), max_length=100)
    from_long = models.CharField(_("من خط العرض"), max_length=100)

    to_country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="to_country",
                                   verbose_name=_("الى الدولة"))
    to_province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="to_province", verbose_name=_("الى المحافظة"))
    to_name = models.CharField(_("الى الاسم"), max_length=200)
    to_lat = models.CharField(_("الى خط الطول"), max_length=100, null=True, blank=True)
    to_long = models.CharField(_("الى خط العرض"), max_length=100, null=True, blank=True)

    distance = models.CharField(_("المسافة"), max_length=10, default=0)

    employee = models.ForeignKey('core.Admin', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name=_("الموظف"), )
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)


class OrderOffer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, )
    company = models.ForeignKey('deliverycompany.DeliveryCompany', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("الناقل"))
    captain = models.ForeignKey('captain.Captain', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("السائق"))
    time = models.TimeField(auto_now_add=True)
    price = models.IntegerField(default=0)
    is_active = models.BooleanField(_("فعال؟"), default=True)
    updated = models.DateTimeField(_("تاريخ اخر تحديث"), auto_now=True)
    created = models.DateTimeField(_("تاريخ الانشاء"), auto_now_add=True)
