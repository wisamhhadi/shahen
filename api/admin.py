from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from captain.models import Captain, CaptainToken
from deliverycompany.models import DeliveryCompany
from mandob.models import Mandob, OrderReport
from order.models import Order
from user.models import User as ClientUser


def get_list_display(model):
    preferred_fields = [
        "id",
        "name",
        "phone",
        "company_name",
        "order_type",
        "user",
        "company",
        "captain",
        "status",
        "order_status",
        "captain_status",
        "client_status",
        "is_active",
        "is_logged",
        "city",
        "location",
        "latitude",
        "longitude",
        "distance",
        "created",
        "updated",
    ]

    model_fields = {
        field.name
        for field in model._meta.fields
    }

    result = [
        field
        for field in preferred_fields
        if field in model_fields
    ]

    if result:
        return result

    return [
        field.name
        for field in model._meta.fields[:8]
    ]


def get_search_fields(model):
    searchable_types = [
        "CharField",
        "TextField",
        "EmailField",
        "SlugField",
    ]

    result = []

    for field in model._meta.fields:
        if field.get_internal_type() in searchable_types:
            result.append(field.name)

    return result


def get_list_filter(model):
    result = []

    for field in model._meta.fields:
        field_type = field.get_internal_type()

        if field_type == "BooleanField":
            result.append(field.name)

        elif getattr(field, "choices", None):
            result.append(field.name)

    return result[:8]


def create_admin_class(model):
    return type(
        f"{model.__name__}Admin",
        (admin.ModelAdmin,),
        {
            "list_display": get_list_display(model),
            "search_fields": get_search_fields(model),
            "list_filter": get_list_filter(model),
            "ordering": ("-id",),
            "list_per_page": 50,
        },
    )


models_to_register = [
    Captain,
    CaptainToken,
    DeliveryCompany,
    Mandob,
    OrderReport,
    Order,
    ClientUser,
]


for model in models_to_register:
    try:
        admin.site.register(model, create_admin_class(model))
    except AlreadyRegistered:
        pass
    