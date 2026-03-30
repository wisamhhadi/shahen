from django.core.management.base import BaseCommand
from core.models import Menu,MenuItem


class Command(BaseCommand):
    help = 'create sidebar default menu'

    def handle(self, *args, **options):
        menu = Menu.objects.create(name="القائمة الافتراضية")

        # الرئيسية (Home)
        MenuItem.objects.create(menu=menu, parent=None, name="الرئيسية", link="/", icon="fas fa-home", order="1",
                                is_active=True)

        # المستخدمين (Users)
        p1 = MenuItem.objects.create(menu=menu, parent=None, name="المستخدمين", link="", icon="fas fa-users", order="2",
                                     is_active=True)
        MenuItem.objects.create(menu=menu, parent=p1, name="الموظفين", link="/list_admin", icon="fas fa-user-tie",
                                order="1", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p1, name="الناقلين", link="/list_delivery_company",
                                icon="fas fa-shipping-fast", order="2", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p1, name="السائقين", link="/list_captain", icon="fas fa-user-check",
                                order="3", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p1, name="الزبائن", link="/list_user", icon="fas fa-user-friends",
                                order="4", is_active=True)

        # المندوبين (Representatives)
        p2 = MenuItem.objects.create(menu=menu, parent=None, name="المندوبين", link="", icon="fas fa-user-cog",
                                     order="3", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="جميع المندوبين", link="/list_mandob",
                                icon="fas fa-users-cog", order="1", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="التقارير الاستبيانية", link="/list_custom_reports",
                                icon="fas fa-poll", order="2", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="التقارير الدورية", link="/list_report",
                                icon="fas fa-chart-line", order="3", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="تقارير الفواتير", link="/list_order_report",
                                icon="fas fa-file-invoice-dollar", order="4", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="الاسئلة اليومية", link="/day_mandob_question_view",
                                icon="fas fa-calendar-day", order="5", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="الاسئلة الاسبوعية", link="/week_mandob_question_view",
                                icon="fas fa-calendar-week", order="6", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="الاسئلة الشهرية", link="/month_mandob_question_view",
                                icon="fas fa-calendar-alt", order="7", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p2, name="الاسئلة السنوية", link="/year_mandob_question_view",
                                icon="fas fa-calendar", order="8", is_active=True)

        # الشحنات (Shipments)
        MenuItem.objects.create(menu=menu, parent=None, name="الشحنات", link="/list_order", icon="fas fa-boxes",
                                order="4", is_active=True)

        # المركبات (Vehicles)
        MenuItem.objects.create(menu=menu, parent=None, name="المركبات", link="/list_car", icon="fas fa-truck",
                                order="5", is_active=True)

        # محاسبة (Accounting)
        p3 = MenuItem.objects.create(menu=menu, parent=None, name="محاسبة", link="", icon="fas fa-calculator",
                                     order="6", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p3, name="سحب وايداع الرصيد", link="/list_pay",
                                icon="fas fa-exchange-alt", order="1", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p3, name="اكواد الرصيد", link="/list_pre_paid", icon="fas fa-qrcode",
                                order="2", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p3, name="الغرامات", link="/list_fine",
                                icon="fas fa-exclamation-triangle", order="3", is_active=True)

        # تعريفات النظام (System Definitions)
        p4 = MenuItem.objects.create(menu=menu, parent=None, name="تعريفات النظام", link="", icon="fas fa-cogs",
                                     order="7", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="الدول", link="/country_view", icon="fas fa-globe",
                                order="1", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="المحافظات", link="/list_province",
                                icon="fas fa-map-marked-alt", order="2", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="التخصصات", link="/specialty_view",
                                icon="fas fa-graduation-cap", order="3", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="اللغات", link="/language_view", icon="fas fa-language",
                                order="4", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="الانشطة", link="/activity_type_view", icon="fas fa-tasks",
                                order="5", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="الاحرف", link="/car_letter_view", icon="fas fa-font",
                                order="6", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="انواع الحمولة", link="/goods_type_view",
                                icon="fas fa-cubes", order="7", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="احجام السيارات", link="/car_size_view",
                                icon="fas fa-ruler-combined", order="8", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="شركات السيارات", link="/car_company_view",
                                icon="fas fa-industry", order="9", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="الوان السيارات", link="/car_color_view",
                                icon="fas fa-palette", order="10", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="فئات السيارات", link="/car_category_view",
                                icon="fas fa-car", order="11", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="انواع المقطورات", link="/list_trailer",
                                icon="fas fa-trailer", order="12", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="موديلات السيارات", link="/car_model_view",
                                icon="fas fa-car-side", order="13", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="بنرات التطبيق", link="/banner_view", icon="fas fa-image",
                                order="14", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p4, name="المدونة", link="/blog_view", icon="fas fa-blog", order="15",
                                is_active=True)

        # اخرى (Others)
        p5 = MenuItem.objects.create(menu=menu, parent=None, name="اخرى", link="", icon="fas fa-ellipsis-h", order="8",
                                     is_active=True)
        MenuItem.objects.create(menu=menu, parent=p5, name="اشعارات", link="/list_notification", icon="fas fa-bell",
                                order="1", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p5, name="اعدادات", link="/update_info/1", icon="fas fa-cog",
                                order="2", is_active=True)
        MenuItem.objects.create(menu=menu, parent=p5, name="قوائم", link="", icon="fas fa-list-ul", order="3",
                                is_active=True)

