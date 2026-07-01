
from datetime import date, time
from django.db import models
from django.utils import timezone

from captain.models import Captain
from user.models import User as ClientUser
from deliverycompany.models import DeliveryCompany
from order.models import Order


def field_value(model, field):
    name = field.name

    if isinstance(field, (models.CharField, models.TextField)):
        if name == "phone":
            return "0780000000"
        if name in ["name", "company_name"]:
            return f"{model.__name__} تجريبي"
        if name == "order_type":
            return "normal"
        if name in ["client_status", "captain_status", "status"]:
            return "pending"
        if name == "distance":
            return "10"
        if name == "collection_area":
            return "بغداد"
        if name == "collection_area_details":
            return "طلب تجريبي من بغداد إلى البصرة"
        return "test"

    if isinstance(field, (models.IntegerField, models.BigIntegerField, models.PositiveIntegerField)):
        return 0

    if isinstance(field, models.BooleanField):
        return True if name == "is_active" else False

    if isinstance(field, models.DateField):
        return date.today()

    if isinstance(field, models.DateTimeField):
        return timezone.now()

    if isinstance(field, models.TimeField):
        return time(9, 0)

    if isinstance(field, (models.FileField, models.ImageField)):
        return ""

    return None


def make_object(model, presets=None):
    presets = presets or {}

    if model.objects.exists():
        return model.objects.first()

    data = dict(presets)
    missing = []

    for f in model._meta.fields:
        if (
            f.name in data
            or f.primary_key
            or f.name in ["password", "last_login"]
            or f.null
            or f.has_default()
            or getattr(f, "auto_now", False)
            or getattr(f, "auto_now_add", False)
        ):
            continue

        if isinstance(f, (models.ForeignKey, models.OneToOneField)):
            related_model = f.remote_field.model

            if related_model.objects.exists():
                data[f.name] = related_model.objects.first()
            else:
                related_obj = make_object(related_model)
                if related_obj is None:
                    missing.append(f"{f.name} -> {related_model.__name__}")
                else:
                    data[f.name] = related_obj
        else:
            data[f.name] = field_value(model, f)

    if missing:
        print("MISSING for", model.__name__)
        for item in missing:
            print("-", item)
        return None

    obj = model(**data)

    if hasattr(obj, "set_password"):
        obj.set_password("11111111")

    obj.save()
    print("CREATED:", model.__name__, obj.pk)
    return obj


captain = Captain.objects.get(phone=7810086970)

client = make_object(ClientUser, {
    "phone": "0780000001",
    "name": "عميل تجريبي",
    "is_active": True,
})

company = make_object(DeliveryCompany, {
    "phone": "0780000002",
    "name": "شركة نقل تجريبية",
    "is_active": True,
})

order_data = {
    "user": client,
    "company": company,
    "captain": captain,
    "collection_area": "بغداد",
    "collection_area_details": "طلب تجريبي من بغداد إلى البصرة",
    "distance": "550",
    "order_type": "normal",
    "captain_status": "pending",
    "client_status": "pending",
    "is_active": True,
}

data = dict(order_data)

for f in Order._meta.fields:
    if (
        f.name in data
        or f.primary_key
        or f.null
        or f.has_default()
        or getattr(f, "auto_now", False)
        or getattr(f, "auto_now_add", False)
    ):
        continue

    if isinstance(f, (models.ForeignKey, models.OneToOneField)):
        related_model = f.remote_field.model
        data[f.name] = related_model.objects.first()
    else:
        data[f.name] = field_value(Order, f)

order = Order.objects.create(**data)

print("ORDER CREATED:", order.id)
print("Captains:", Captain.objects.count())
print("Users:", ClientUser.objects.count())
print("Companies:", DeliveryCompany.objects.count())
print("Orders:", Order.objects.count())

