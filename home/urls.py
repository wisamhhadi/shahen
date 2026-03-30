from .auto_completes import *
from .excels import *
from .views.admin import *
from .views.attendance import *
from .views.captain import *
from .views.car import *
from .views.custom_report import create_custom_report, list_custom_reports, update_custom_report, delete_custom_report
from .views.delivery_company import *
from .views.extra import *
from .views.home import *
from .views.mandob import *
from .views.map import mandob_map, captain_map, mandob_autocomplete_map, captain_autocomplete_map
from .views.order import *
from .views.pay import *
from home.views.fine import *
from .views.pre_paid import *
from .views.province import *
from .views.trailer import *
from .views.user import *
from .views.notification import *
from django.urls import path


urlpatterns = [
    path('', index, name='home'),
    path('profile', profile.as_view(), name='profile'),
    path('logout', logout_page, name='logout'),
    path('login', login_page, name='login'),
    path('mandob_map', mandob_map, name='mandob_map'),
    path('captain_map', captain_map, name='captain_map'),
    path('chat/<int:mandob_id>', chat_room, name='chat'),
    path('captain_chat/<int:captain_id>', captain_chat, name='captain_chat'),
    path('user_chat/<int:user_id>', user_chat, name='user_chat'),

    path('mandob_autocomplete_map', mandob_autocomplete_map, name='mandob_autocomplete_map'),
    path('captain_autocomplete_map', captain_autocomplete_map, name='captain_autocomplete_map'),

    path('list_admin', list_admin.as_view(), name='list_admin'),
    path('create_admin', create_admin.as_view(), name='create_admin'),
    path('update_admin/<int:pk>', update_admin.as_view(), name='update_admin'),
    path('delete_admin/<int:pk>', delete_admin.as_view(), name='delete_admin'),

    path('list_mandob', list_mandob.as_view(), name='list_mandob'),
    path('create_mandob', create_mandob.as_view(), name='create_mandob'),
    path('update_mandob/<int:pk>', update_mandob.as_view(), name='update_mandob'),
    path('delete_mandob/<int:pk>', delete_mandob.as_view(), name='delete_mandob'),

    path('list_history', list_history.as_view(), name='list_history'),
    path('list_attendance', list_attendance.as_view(), name='list_attendance'),
    path('create_attendance', create_attendance.as_view(), name='create_attendance'),

    path('list_report', list_report.as_view(), name='list_report'),
    path('update_report/<int:pk>', update_report.as_view(), name='update_report'),
    path('delete_report/<int:pk>', delete_report.as_view(), name='delete_report'),

    path('list_order_report', list_order_report.as_view(), name='list_order_report'),
    path('update_order_report/<int:pk>', update_order_report.as_view(), name='update_order_report'),
    path('delete_order_report/<int:pk>', delete_order_report.as_view(), name='delete_order_report'),

    path('list_custom_reports', list_custom_reports.as_view(), name='list_custom_reports'),
    path('create_custom_report', create_custom_report, name='create_custom_report'),
    path('update_custom_report/<int:pk>', update_custom_report, name='update_custom_report'),
    path('delete_custom_report/<int:pk>', delete_custom_report, name='delete_custom_report'),


    path('list_province', list_province.as_view(), name='list_province'),
    path('create_province', create_province.as_view(), name='create_province'),
    path('update_province/<int:pk>', update_province.as_view(), name='update_province'),
    path('delete_province/<int:pk>', delete_province.as_view(), name='delete_province'),

    path('list_trailer', list_trailer.as_view(), name='list_trailer'),
    path('create_trailer', create_trailer.as_view(), name='create_trailer'),
    path('update_trailer/<int:pk>', update_trailer.as_view(), name='update_trailer'),
    path('delete_trailer/<int:pk>', delete_trailer.as_view(), name='delete_trailer'),

    path('list_delivery_company', list_delivery_company.as_view(), name='list_delivery_company'),
    path('create_delivery_company', create_delivery_company.as_view(), name='create_delivery_company'),
    path('update_delivery_company/<int:pk>', update_delivery_company.as_view(), name='update_delivery_company'),
    path('delete_delivery_company/<int:pk>', delete_delivery_company.as_view(), name='delete_delivery_company'),

    path('list_car', list_car.as_view(), name='list_car'),
    path('create_car', create_car.as_view(), name='create_car'),
    path('update_car/<int:pk>', update_car.as_view(), name='update_car'),
    path('delete_car/<int:pk>', delete_car.as_view(), name='delete_car'),

    path('list_captain', list_captain.as_view(), name='list_captain'),
    path('create_captain', create_captain.as_view(), name='create_captain'),
    path('update_captain/<int:pk>', update_captain.as_view(), name='update_captain'),
    path('delete_captain/<int:pk>', delete_captain.as_view(), name='delete_captain'),

    path('list_user', list_user.as_view(), name='list_user'),
    path('create_user', create_user.as_view(), name='create_user'),
    path('update_user/<int:pk>', update_user.as_view(), name='update_user'),
    path('delete_user/<int:pk>', delete_user.as_view(), name='delete_user'),

    path('list_order', list_order.as_view(), name='list_order'),
    path('create_order', create_order.as_view(), name='create_order'),
    path('update_order/<int:pk>', update_order.as_view(), name='update_order'),
    path('delete_order/<int:pk>', delete_order.as_view(), name='delete_order'),

    path('list_pay', list_pay.as_view(), name='list_pay'),
    path('create_pay', create_pay.as_view(), name='create_pay'),
    path('update_pay/<int:pk>', update_pay.as_view(), name='update_pay'),
    path('delete_pay/<int:pk>', delete_pay.as_view(), name='delete_pay'),

    path('list_fine', list_fine.as_view(), name='list_fine'),
    path('create_fine', create_fine.as_view(), name='create_fine'),
    path('update_fine/<int:pk>', update_fine.as_view(), name='update_fine'),
    path('delete_fine/<int:pk>', delete_fine.as_view(), name='delete_fine'),

    path('list_pre_paid', list_pre_paid.as_view(), name='list_pre_paid'),
    path('create_pre_paid', create_pre_paid.as_view(), name='create_pre_paid'),
    path('update_pre_paid/<int:pk>', update_pre_paid.as_view(), name='update_pre_paid'),
    path('delete_pre_paid/<int:pk>', delete_pre_paid.as_view(), name='delete_pre_paid'),

    path('list_notification', list_notification.as_view(), name='list_notification'),
    path('create_notification', create_notification.as_view(), name='create_notification'),
    path('update_notification/<int:pk>', update_notification.as_view(), name='update_notification'),
    path('delete_notification/<int:pk>', delete_notification.as_view(), name='delete_notification'),

    path('update_info/<int:pk>', update_info.as_view(), name='update_info'),

    path('language_view', language_view, name='language_view'),
    path('country_view', country_view, name='country_view'),
    path('specialty_view', specialty_view, name='specialty_view'),
    path('car_company_view', car_company_view, name='car_company_view'),
    path('car_model_view', car_model_view, name='car_model_view'),
    path('car_color_view', car_color_view, name='car_color_view'),
    path('car_category_view', car_category_view, name='car_category_view'),
    path('car_letter_view', car_letter_view, name='car_letter_view'),
    path('car_size_view', car_size_view, name='car_size_view'),
    path('activity_type_view', activity_type_view, name='activity_type_view'),
    path('goods_type_view', goods_type_view, name='goods_type_view'),
    path('banner_view', banner_view, name='banner_view'),
    path('blog_view', blog_view, name='blog_view'),
    path('day_mandob_question_view', day_mandob_question_view, name='day_mandob_question_view'),
    path('week_mandob_question_view', week_mandob_question_view, name='week_mandob_question_view'),
    path('month_mandob_question_view', month_mandob_question_view, name='month_mandob_question_view'),
    path('year_mandob_question_view', year_mandob_question_view, name='year_mandob_question_view'),
    path('custom_mandob_question_view', custom_mandob_question_view, name='custom_mandob_question_view'),

    path('permission_group_autocomplete', permission_group_autocomplete.as_view(), name='permission_group_autocomplete'),
    path('admin_autocomplete', admin_autocomplete.as_view(), name='admin_autocomplete'),
    path('mandob_autocomplete', mandob_autocomplete.as_view(), name='mandob_autocomplete'),
    path('country_autocomplete', country_autocomplete.as_view(), name='country_autocomplete'),
    path('province_autocomplete', province_autocomplete.as_view(), name='province_autocomplete'),
    path('delivery_company_autocomplete', delivery_company_autocomplete.as_view(), name='delivery_company_autocomplete'),
    path('trailer_autocomplete', trailer_autocomplete.as_view(), name='trailer_autocomplete'),
    path('car_autocomplete', car_autocomplete.as_view(), name='car_autocomplete'),
    path('captain_autocomplete', captain_autocomplete.as_view(), name='captain_autocomplete'),
    path('user_autocomplete', user_autocomplete.as_view(), name='user_autocomplete'),


    path('admin_excel', admin_excel.as_view(), name='admin_excel'),
    path('language_excel', language_excel.as_view(), name='language_excel'),
    path('mandob_excel', mandob_excel.as_view(), name='mandob_excel'),
    path('attendance_excel', attendance_excel.as_view(), name='attendance_excel'),
    path('country_excel', country_excel.as_view(), name='country_excel'),
    path('province_excel', province_excel.as_view(), name='province_excel'),
    path('specialty_excel', specialty_excel.as_view(), name='specialty_excel'),
    path('car_company_excel', car_company_excel.as_view(), name='car_company_excel'),
    path('car_model_excel', car_model_excel.as_view(), name='car_model_excel'),
    path('car_color_excel', car_color_excel.as_view(), name='car_color_excel'),
    path('car_category_excel', car_category_excel.as_view(), name='car_category_excel'),
    path('goods_type_excel', goods_type_excel.as_view(), name='goods_type_excel'),
    path('trailer_excel', trailer_excel.as_view(), name='trailer_excel'),
    path('car_letter_excel', car_letter_excel.as_view(), name='car_letter_excel'),
    path('car_size_excel', car_size_excel.as_view(), name='car_size_excel'),
    path('activity_type_excel', activity_type_excel.as_view(), name='activity_type_excel'),
    path('delivery_company_excel', delivery_company_excel.as_view(), name='delivery_company_excel'),
    path('car_excel', car_excel.as_view(), name='car_excel'),
    path('captain_excel', captain_excel.as_view(), name='captain_excel'),
    path('user_excel', user_excel.as_view(), name='user_excel'),
    path('order_excel', order_excel.as_view(), name='order_excel'),
    path('order_car_excel', order_car_excel.as_view(), name='order_car_excel'),
    path('pay_excel', pay_excel.as_view(), name='pay_excel'),
    path('pre_paid_excel', pre_paid_excel.as_view(), name='pre_paid_excel'),


]