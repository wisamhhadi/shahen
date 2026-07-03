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
from order.models import Order, OrderCar, OrderOffer
from core.models import Car

from .serializers import (
    DeliveryCompanySerializer,
    CaptainSerializer,
    OrderSerializer,
)

TRANSPORTER_TOKEN_SALT = "transporter-mobile-token"


def _make_token(transporter):
    return signing.dumps(
        {"type": "transporter", "id": transporter.id},
        salt=TRANSPORTER_TOKEN_SALT,
    )


def _get_transporter_by_phone(phone):
    phone_text = str(phone).strip()
    digits = "".join(ch for ch in phone_text if ch.isdigit())

    candidates = [digits]
    if digits.startswith("0"):
        candidates.append(digits[1:])

    for item in candidates:
        if not item:
            continue

        try:
            return DeliveryCompany.objects.get(phone=item)
        except DeliveryCompany.DoesNotExist:
            pass

        try:
            return DeliveryCompany.objects.get(phone=str(int(item)))
        except Exception:
            pass

    return None


def _check_password(transporter, raw_password):
    stored = str(getattr(transporter, "password", "") or "")

    if hasattr(transporter, "check_password"):
        try:
            if transporter.check_password(raw_password):
                return True
        except Exception:
            pass

    try:
        if check_password(raw_password, stored):
            return True
    except Exception:
        pass

    return stored == str(raw_password)


def _get_transporter_from_token(request):
    auth_header = (
        request.META.get("HTTP_AUTHORIZATION")
        or request.headers.get("Authorization")
        or ""
    ).strip()

    token = ""

    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() in [
            "token",
            "bearer",
            "transportertoken",
        ]:
            token = parts[1].strip()
        else:
            token = (
                auth_header
                .replace("TransporterToken", "")
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


def _file_url(request, file_obj):
    if not file_obj:
        return None

    try:
        return request.build_absolute_uri(file_obj.url)
    except Exception:
        try:
            return file_obj.url
        except Exception:
            return None


def transporter_data(transporter, request):
    data = DeliveryCompanySerializer(
        transporter,
        context={"request": request},
    ).data

    data.update({
        "id": transporter.id,
        "name": getattr(transporter, "name", None),
        "phone": getattr(transporter, "phone", None),
        "city": getattr(transporter, "city", None),
        "location": getattr(transporter, "location", None),
        "is_active": getattr(transporter, "is_active", True),
        "is_logged": getattr(transporter, "is_logged", False),
        "balance": getattr(transporter, "balance", 0),
        "latitude": getattr(transporter, "latitude", None),
        "longitude": getattr(transporter, "longitude", None),
        "latitude_base": getattr(transporter, "latitude_base", None),
        "longitude_base": getattr(transporter, "longitude_base", None),
        "image_url": _file_url(request, getattr(transporter, "image", None)),
    })

    return data


def driver_data(driver, request):
    data = CaptainSerializer(driver, context={"request": request}).data
    car = getattr(driver, "car", None)

    data.update({
        "id": driver.id,
        "name": getattr(driver, "name", None),
        "phone": getattr(driver, "phone", None),
        "status": getattr(driver, "status", None),
        "is_active": getattr(driver, "is_active", True),
        "is_logged": getattr(driver, "is_logged", False),
        "latitude": getattr(driver, "latitude", None),
        "longitude": getattr(driver, "longitude", None),
        "latitude_base": getattr(driver, "latitude_base", None),
        "longitude_base": getattr(driver, "longitude_base", None),
        "image_url": _file_url(request, getattr(driver, "image", None)),
        "car_id": getattr(car, "id", None) if car else None,
        "car_number": getattr(car, "car_number", None) if car else None,
    })

    return data


def vehicle_data(car):
    return {
        "id": car.id,
        "car_number": getattr(car, "car_number", None),
        "name": str(car),
        "captain": getattr(car, "captain_id", None),
        "captain_name": getattr(getattr(car, "captain", None), "name", None),
        "is_active": getattr(car, "is_active", True),
        "balance": getattr(car, "balance", 0),
        "max_balance": getattr(car, "max_balance", 0),
        "car_id_name": getattr(car, "car_id_name", None),
        "car_id_number": getattr(car, "car_id_number", None),
        "car_id_vin": getattr(car, "car_id_vin", None),
        "car_id_expire": getattr(car, "car_id_expire", None),
        "car_manu_year": getattr(car, "car_manu_year", 0),
    }


def order_brief(order):
    first_car = OrderCar.objects.filter(order=order).first()

    return {
        "id": order.id,
        "collection_area": getattr(order, "collection_area", None),
        "collection_area_details": getattr(order, "collection_area_details", None),
        "company": getattr(order, "company_id", None),
        "company_name": getattr(getattr(order, "company", None), "name", None),
        "captain": getattr(order, "captain_id", None),
        "captain_name": getattr(getattr(order, "captain", None), "name", None),
        "captain_status": getattr(order, "captain_status", None),
        "client_status": getattr(order, "client_status", None),
        "order_type": getattr(order, "order_type", None),
        "distance": getattr(order, "distance", None),
        "note": getattr(order, "note", None),
        "is_active": getattr(order, "is_active", True),
        "created": getattr(order, "created", None),
        "updated": getattr(order, "updated", None),
        "from_name": getattr(first_car, "from_name", None) if first_car else None,
        "from_lat": getattr(first_car, "from_lat", None) if first_car else None,
        "from_long": getattr(first_car, "from_long", None) if first_car else None,
        "to_name": getattr(first_car, "to_name", None) if first_car else None,
        "to_lat": getattr(first_car, "to_lat", None) if first_car else None,
        "to_long": getattr(first_car, "to_long", None) if first_car else None,
    }


def stats_data(transporter):
    drivers = Captain.objects.filter(company=transporter)
    vehicles = Car.objects.filter(company=transporter)
    orders = Order.objects.filter(company=transporter)

    active_orders = orders.filter(is_active=True)

    completed_orders = orders.filter(
        Q(captain_status__icontains="complete") |
        Q(captain_status__icontains="completed") |
        Q(captain_status__icontains="تم") |
        Q(client_status__icontains="complete") |
        Q(client_status__icontains="completed")
    )

    rejected_orders = orders.filter(
        Q(captain_status__icontains="reject") |
        Q(captain_status__icontains="rejected") |
        Q(captain_status__icontains="رفض")
    )

    committed_vehicles = Car.objects.filter(
        id__in=OrderCar.objects.filter(order__company=transporter).values_list("car_id", flat=True)
    ).distinct()

    return {
        "drivers_count": drivers.count(),
        "vehicles_count": vehicles.count(),
        "orders_count": orders.count(),
        "active_orders_count": active_orders.count(),
        "completed_orders_count": completed_orders.count(),
        "rejected_orders_count": rejected_orders.count(),
        "committed_vehicles_count": committed_vehicles.count(),
        "drivers_need_help_count": 0,
        "stopped_drivers_count": 0,
        "late_loading_drivers_count": 0,
        "maintenance_vehicles_count": 0,
    }


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

    transporter = _get_transporter_by_phone(phone)

    if transporter is None or not _check_password(transporter, password):
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if hasattr(transporter, "is_active") and not transporter.is_active:
        return Response(
            {"detail": "Transporter account is inactive"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if hasattr(transporter, "is_logged"):
        transporter.is_logged = True
        try:
            transporter.save(update_fields=["is_logged"])
        except Exception:
            transporter.save()

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
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({
        "transporter": transporter_data(transporter, request),
        "stats": stats_data(transporter),
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_stats(request):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response(stats_data(transporter))


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_drivers(request):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    qs = Captain.objects.filter(company=transporter).order_by("-id")

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(city__icontains=search) |
            Q(location__icontains=search) |
            Q(status__icontains=search)
        )

    return Response([driver_data(item, request) for item in qs])


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_vehicles(request):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    qs = Car.objects.filter(company=transporter).order_by("-id")
    return Response([vehicle_data(item) for item in qs])


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_orders(request):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    qs = Order.objects.filter(company=transporter).order_by("-id")

    # يعرض الطلبات الفعالة غير المخصصة أيضاً حتى يستطيع الناقل قبولها عند الحاجة.
    if request.GET.get("include_open") == "1":
        qs = Order.objects.filter(
            Q(company=transporter) | Q(company__isnull=True),
            is_active=True,
        ).order_by("-id")

    return Response([order_brief(item) for item in qs])


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_assign_order(request, pk):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    driver_id = request.data.get("driver_id")
    vehicle_id = request.data.get("vehicle_id")

    if not driver_id:
        return Response(
            {"detail": "driver_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        driver = Captain.objects.get(pk=driver_id, company=transporter)
    except Captain.DoesNotExist:
        return Response(
            {"detail": "Driver not found for this transporter"},
            status=status.HTTP_404_NOT_FOUND,
        )

    vehicle = None

    if vehicle_id:
        try:
            vehicle = Car.objects.get(pk=vehicle_id, company=transporter)
        except Car.DoesNotExist:
            return Response(
                {"detail": "Vehicle not found for this transporter"},
                status=status.HTTP_404_NOT_FOUND,
            )

    order.company = transporter
    order.captain = driver

    if hasattr(order, "captain_status"):
        order.captain_status = "accepted"

    order.save()

    order_car = OrderCar.objects.filter(order=order).first()

    if order_car:
        order_car.captain = driver
        if vehicle:
            order_car.car = vehicle
        order_car.save()

    return Response({
        "detail": "Order assigned successfully",
        "order": order_brief(order),
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_wallet(request):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({
        "balance": getattr(transporter, "balance", 0),
        "currency": "IQD",
        "items": [],
    })


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_send_notification(request):
    transporter = _get_transporter_from_token(request)

    if transporter is None:
        return Response(
            {"detail": "Invalid or missing transporter token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({
        "detail": "Notification endpoint is ready. Firebase integration comes next.",
        "sent": False,
    })


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_logout(request):
    transporter = _get_transporter_from_token(request)

    if transporter is not None and hasattr(transporter, "is_logged"):
        transporter.is_logged = False
        try:
            transporter.save(update_fields=["is_logged"])
        except Exception:
            transporter.save()

    return Response({"detail": "Logged out successfully"})
