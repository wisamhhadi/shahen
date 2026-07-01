from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.api_login, name="api_login"),
    path("me/", views.api_me, name="api_me"),

    path("mandobs/", views.api_mandobs, name="api_mandobs"),
    path("mandobs/<int:pk>/", views.api_mandob_detail, name="api_mandob_detail"),

    path("captains/", views.api_captains, name="api_captains"),
    path("captains/<int:pk>/", views.api_captain_detail, name="api_captain_detail"),

    path("delivery-companies/", views.api_delivery_companies, name="api_delivery_companies"),
    path("delivery-companies/<int:pk>/", views.api_delivery_company_detail, name="api_delivery_company_detail"),

    path("users/", views.api_users, name="api_users"),
    path("users/<int:pk>/", views.api_user_detail, name="api_user_detail"),

    path("orders/", views.api_orders, name="api_orders"),
    path("orders/<int:pk>/", views.api_order_detail, name="api_order_detail"),

    path("order-reports/", views.api_order_reports, name="api_order_reports"),
    path("order-reports/<int:pk>/", views.api_order_report_detail, name="api_order_report_detail"),
    path("captain/login/", views.api_captain_login, name="api_captain_login"),
    path("captain/me/", views.api_captain_me, name="api_captain_me"),
    path("captain/orders/", views.api_captain_orders, name="api_captain_orders"),
]