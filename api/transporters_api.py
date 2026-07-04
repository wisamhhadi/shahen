from django.core import signing
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from deliverycompany.models import DeliveryCompany
from captain.models import Captain
from order.models import Order

try:
    from core.models import Car
except Exception:
    Car = None

from .serializers import DeliveryCompanySerializer, CaptainSerializer, OrderSerializer

TRANSPORTER_TOKEN_SALT = "transporter-mobile-token"


def _model_has_field(model, field_name):
    try:
        model._meta.get_field(field_name)
        return True
    except Exception:
        return False


def _field_names(model):
    try:
        return {field.name for field in model._meta.fields}
    except Exception:
        return set()


def _set_if_field(obj, field, value):
    if value is None:
        return False

    if _model_has_field(obj.__class__, field):
        setattr(obj, field, value)
        return True

    return False


def _safe_int_or_text(value):
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    digits = "".join(ch for ch in text if ch.isdigit())

    if digits:
        try:
            return int(digits)
        except Exception:
            return digits

    return text


def _make_token(transporter):
    return signing.dumps(
        {"type": "transporter", "id": transporter.id},
        salt=TRANSPORTER_TOKEN_SALT,
    )


def _get_by_phone(phone):
    txt = str(phone).strip()
    digits = "".join(ch for ch in txt if ch.isdigit())

    candidates = [digits]
    if digits.startswith("0"):
        candidates.append(digits[1:])

    for value in candidates:
        if not value:
            continue

        try:
            return DeliveryCompany.objects.get(phone=int(value))
        except Exception:
            pass

        try:
            return DeliveryCompany.objects.get(phone=value)
        except Exception:
            pass

    return None


def _check_password(obj, raw_password):
    stored = str(getattr(obj, "password", "") or "")

    if hasattr(obj, "check_password"):
        try:
            if obj.check_password(raw_password):
                return True
        except Exception:
            pass

    try:
        if check_password(raw_password, stored):
            return True
    except Exception:
        pass

    return stored == str(raw_password)


def _get_from_token(request):
    header = (
        request.META.get("HTTP_AUTHORIZATION")
        or request.headers.get("Authorization")
        or ""
    ).strip()

    token = ""

    if header:
        parts = header.split()
        if len(parts) == 2 and parts[0].lower() in ["token", "bearer", "transportertoken"]:
            token = parts[1].strip()
        else:
            token = (
                header.replace("TransporterToken", "")
                .replace("Bearer", "")
                .replace("Token", "")
                .strip()
            )

    if not token:
        token = request.GET.get("token", "").strip()

    if not token:
        return None

    try:
        data = signing.loads(
            token,
            salt=TRANSPORTER_TOKEN_SALT,
            max_age=60 * 60 * 24 * 365,
        )

        if data.get("type") != "transporter":
            return None

        return DeliveryCompany.objects.get(pk=data.get("id"))
    except Exception:
        return None


def _filter_owned(qs, owner):
    model = qs.model

    for field in ["company", "delivery_company", "deliverycompany", "transporter", "owner"]:
        if _model_has_field(model, field):
            try:
                return qs.filter(**{field: owner})
            except Exception:
                pass

    return qs.none()


def _count(qs):
    try:
        return qs.count()
    except Exception:
        return 0


def transporter_data(obj, request=None):
    data = DeliveryCompanySerializer(obj, context={"request": request}).data

    data["id"] = obj.id
    data["name"] = getattr(obj, "name", None)
    data["phone"] = getattr(obj, "phone", None)
    data["status"] = getattr(obj, "status", None)
    data["is_active"] = getattr(obj, "is_active", True)
    data["is_logged"] = getattr(obj, "is_logged", False)
    data["balance"] = getattr(obj, "balance", 0)
    data["latitude"] = getattr(obj, "latitude", None)
    data["longitude"] = getattr(obj, "longitude", None)
    data["latitude_base"] = getattr(obj, "latitude_base", None)
    data["longitude_base"] = getattr(obj, "longitude_base", None)
    data["city"] = getattr(obj, "city", None)
    data["location"] = getattr(obj, "location", None)
    data["image_url"] = None

    image = getattr(obj, "image", None)
    if image:
        try:
            data["image_url"] = request.build_absolute_uri(image.url) if request else image.url
        except Exception:
            pass

    return data


def stats_data(transporter):
    drivers = _filter_owned(Captain.objects.all(), transporter)
    vehicles = _filter_owned(Car.objects.all(), transporter) if Car else None
    orders = _filter_owned(Order.objects.all(), transporter)

    return {
        "drivers_count": _count(drivers),
        "vehicles_count": _count(vehicles) if vehicles is not None else 0,
        "orders_count": _count(orders),
        "active_orders_count": _count(orders.filter(is_active=True)) if _model_has_field(Order, "is_active") else _count(orders),
        "completed_orders_count": 0,
        "rejected_orders_count": 0,
        "drivers_need_help_count": 0,
        "stopped_drivers_count": 0,
        "late_loading_drivers_count": 0,
        "maintenance_vehicles_count": 0,
        "committed_vehicles_count": 0,
    }


def _auth_or_401(request):
    transporter = _get_from_token(request)

    if transporter is None:
        return None, Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return transporter, None


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_login(request):
    phone = request.data.get("phone")
    password = request.data.get("password")

    if not phone or not password:
        return Response(
            {"detail": "phone and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    transporter = _get_by_phone(phone)

    if transporter is None or not _check_password(transporter, password):
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if hasattr(transporter, "is_active") and not transporter.is_active:
        return Response(
            {"detail": "Transporter is inactive"},
            status=status.HTTP_403_FORBIDDEN,
        )

    token = _make_token(transporter)

    return Response({
        "id": transporter.id,
        "token": token,
        "transporter": transporter_data(transporter, request),
        "stats": stats_data(transporter),
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_me(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    return Response({
        "transporter": transporter_data(transporter, request),
        "stats": stats_data(transporter),
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_stats(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    return Response(stats_data(transporter))


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_drivers(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    qs = _filter_owned(Captain.objects.all().order_by("-id"), transporter)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search)
            | Q(phone__icontains=search)
            | Q(city__icontains=search)
            | Q(location__icontains=search)
        )

    return Response(CaptainSerializer(qs, many=True, context={"request": request}).data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_create_driver(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    name = str(request.data.get("name") or "").strip()
    phone = request.data.get("phone")
    password = str(request.data.get("password") or "123456").strip()

    if not name:
        return Response({"detail": "اسم السائق مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    if not phone:
        return Response({"detail": "رقم الهاتف مطلوب"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        driver = Captain()

        _set_if_field(driver, "name", name)
        _set_if_field(driver, "phone", _safe_int_or_text(phone))
        _set_if_field(driver, "city", request.data.get("city"))
        _set_if_field(driver, "location", request.data.get("location"))
        _set_if_field(driver, "latitude", request.data.get("latitude"))
        _set_if_field(driver, "longitude", request.data.get("longitude"))
        _set_if_field(driver, "latitude2", request.data.get("latitude"))
        _set_if_field(driver, "longitude2", request.data.get("longitude"))

        for field in ["company", "delivery_company", "deliverycompany", "transporter"]:
            if _set_if_field(driver, field, transporter):
                break

        _set_if_field(driver, "status", "accepted")
        _set_if_field(driver, "is_active", True)
        _set_if_field(driver, "is_free", False)
        _set_if_field(driver, "is_logged", False)

        if hasattr(driver, "set_password"):
            driver.set_password(password)
        elif _model_has_field(Captain, "password"):
            driver.password = password

        driver.save()

        return Response(
            CaptainSerializer(driver, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
    except Exception as exc:
        return Response(
            {"detail": f"تعذر إضافة السائق: {exc}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_vehicles(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    if Car is None:
        return Response([])

    qs = _filter_owned(Car.objects.all().order_by("-id"), transporter)
    data = []

    for car in qs:
        item = model_to_dict(car)
        item["id"] = car.id
        item["display_name"] = (
            getattr(car, "name", None)
            or getattr(car, "number", None)
            or getattr(car, "plate", None)
            or getattr(car, "car_number", None)
            or getattr(car, "car_id_name", None)
            or str(car)
        )
        data.append(item)

    return Response(data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_create_vehicle(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    if Car is None:
        return Response(
            {"detail": "Car model is not available"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    name = str(request.data.get("name") or request.data.get("display_name") or "").strip()
    plate = str(request.data.get("plate") or request.data.get("number") or "").strip()

    if not name and not plate:
        return Response(
            {"detail": "أدخل اسم المركبة أو رقم اللوحة"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        car = Car()

        # ربط المركبة بالناقل
        for field in ["company", "delivery_company", "deliverycompany", "transporter", "owner"]:
            if _set_if_field(car, field, transporter):
                break

        # تعبئة أسماء محتملة حسب موديل core.Car
        for field in ["name", "display_name", "car_name", "car_id_name"]:
            _set_if_field(car, field, name or plate)

        for field in ["plate", "number", "car_number", "car_plate", "plate_number"]:
            _set_if_field(car, field, plate or name)

        _set_if_field(car, "color", request.data.get("color"))
        _set_if_field(car, "model", request.data.get("model"))
        _set_if_field(car, "note", request.data.get("note"))
        _set_if_field(car, "status", request.data.get("status") or "active")
        _set_if_field(car, "is_active", True)

        car.save()

        item = model_to_dict(car)
        item["id"] = car.id
        item["display_name"] = name or plate or str(car)

        return Response(item, status=status.HTTP_201_CREATED)
    except Exception as exc:
        return Response(
            {"detail": f"تعذر إضافة المركبة: {exc}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_orders(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    qs = _filter_owned(Order.objects.all().order_by("-id"), transporter)

    if not qs.exists():
        qs = Order.objects.all().order_by("-id")
        if _model_has_field(Order, "is_active"):
            qs = qs.filter(is_active=True)

    return Response(OrderSerializer(qs, many=True, context={"request": request}).data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_assign_order(request, pk):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    driver_id = request.data.get("driver_id")
    vehicle_id = request.data.get("vehicle_id")

    if not driver_id:
        return Response(
            {"detail": "driver_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        order = Order.objects.get(pk=pk)
        driver = Captain.objects.get(pk=driver_id)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Captain.DoesNotExist:
        return Response({"detail": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

    changed = []

    if _model_has_field(Order, "captain"):
        order.captain = driver
        changed.append("captain")

    for field in ["company", "delivery_company", "deliverycompany", "transporter"]:
        if _model_has_field(Order, field):
            setattr(order, field, transporter)
            changed.append(field)
            break

    if vehicle_id and Car is not None:
        try:
            vehicle = Car.objects.get(pk=vehicle_id)
            for field in ["car", "vehicle"]:
                if _model_has_field(Order, field):
                    setattr(order, field, vehicle)
                    changed.append(field)
                    break
        except Car.DoesNotExist:
            return Response({"detail": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)

    for field, value in [("captain_status", "accepted"), ("status", "assigned"), ("is_active", True)]:
        if _model_has_field(Order, field):
            setattr(order, field, value)
            changed.append(field)

    try:
        order.save(update_fields=list(set(changed)) if changed else None)
    except Exception:
        order.save()

    return Response({
        "detail": "Order assigned successfully",
        "order": OrderSerializer(order, context={"request": request}).data,
    })


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_send_notification(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    return Response({"detail": "Notification endpoint is ready", "sent": False})


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_wallet(request):
    transporter, error = _auth_or_401(request)
    if error:
        return error

    return Response({
        "balance": getattr(transporter, "balance", 0),
        "currency": "IQD",
        "items": [],
    })
