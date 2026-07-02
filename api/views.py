from django.contrib.auth.hashers import check_password
from django.core import signing

from mandob.models import Mandob
from .serializers import MandobSerializer
import secrets
from django.core import signing
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from mandob.models import Mandob, OrderReport
from captain.models import Captain, CaptainToken
from deliverycompany.models import DeliveryCompany
from order.models import Order
from user.models import User as ClientUser

from .serializers import (
    UserProfileSerializer,
    MandobSerializer,
    CaptainSerializer,
    DeliveryCompanySerializer,
    ClientUserSerializer,
    OrderSerializer,
    OrderReportSerializer,
)
MANDOB_TOKEN_SALT = "mandob-mobile-token"
User = get_user_model()


def limit_queryset(request, qs, default=100, max_limit=500):
    try:
        limit = int(request.GET.get("limit", default))
    except ValueError:
        limit = default

    limit = min(limit, max_limit)
    return qs[:limit]


@api_view(["POST"])
@permission_classes([AllowAny])
def api_login(request):
    phone = request.data.get("phone")
    password = request.data.get("password")

    if not phone or not password:
        return Response(
            {"detail": "phone and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=str(phone), password=password)

    if user is None and str(phone).startswith("0"):
        user = authenticate(request, username=str(phone)[1:], password=password)

    if user is None:
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "user": UserProfileSerializer(user).data,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_me(request):
    return Response({
        "user": UserProfileSerializer(request.user).data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_mandobs(request):
    qs = Mandob.objects.all().order_by("-id")

    if request.GET.get("active") == "1":
        qs = qs.filter(is_active=True)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(city__icontains=search) |
            Q(location__icontains=search) |
            Q(status__icontains=search)
        )

    qs = limit_queryset(request, qs)
    return Response(
        MandobSerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_mandob_detail(request, pk):
    try:
        obj = Mandob.objects.get(pk=pk)
    except Mandob.DoesNotExist:
        return Response({"detail": "Mandob not found"}, status=404)

    return Response(MandobSerializer(obj, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_captains(request):
    qs = Captain.objects.all().order_by("-id")

    if request.GET.get("active") == "1":
        qs = qs.filter(is_active=True)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(city__icontains=search) |
            Q(location__icontains=search) |
            Q(status__icontains=search)
        )

    qs = limit_queryset(request, qs)
    return Response(
        CaptainSerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_captain_detail(request, pk):
    try:
        obj = Captain.objects.get(pk=pk)
    except Captain.DoesNotExist:
        return Response({"detail": "Captain not found"}, status=404)

    return Response(CaptainSerializer(obj, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_delivery_companies(request):
    qs = DeliveryCompany.objects.all().order_by("-id")

    if request.GET.get("active") == "1":
        qs = qs.filter(is_active=True)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(city__icontains=search) |
            Q(location__icontains=search)
        )

    qs = limit_queryset(request, qs)
    return Response(
        DeliveryCompanySerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_delivery_company_detail(request, pk):
    try:
        obj = DeliveryCompany.objects.get(pk=pk)
    except DeliveryCompany.DoesNotExist:
        return Response({"detail": "Delivery company not found"}, status=404)

    return Response(DeliveryCompanySerializer(obj, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_users(request):
    qs = ClientUser.objects.all().order_by("-id")

    if request.GET.get("active") == "1":
        qs = qs.filter(is_active=True)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(company_name__icontains=search) |
            Q(city__icontains=search) |
            Q(location__icontains=search)
        )

    qs = limit_queryset(request, qs)
    return Response(
        ClientUserSerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_user_detail(request, pk):
    try:
        obj = ClientUser.objects.get(pk=pk)
    except ClientUser.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    return Response(ClientUserSerializer(obj, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_orders(request):
    qs = Order.objects.all().order_by("-id")

    if request.GET.get("active") == "1":
        qs = qs.filter(is_active=True)

    order_type = request.GET.get("order_type")
    if order_type:
        qs = qs.filter(order_type=order_type)

    client_status = request.GET.get("client_status")
    if client_status:
        qs = qs.filter(client_status=client_status)

    captain_status = request.GET.get("captain_status")
    if captain_status:
        qs = qs.filter(captain_status=captain_status)

    qs = limit_queryset(request, qs)
    return Response(
        OrderSerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_order_detail(request, pk):
    try:
        obj = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=404)

    return Response(OrderSerializer(obj, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_order_reports(request):
    qs = OrderReport.objects.all().order_by("-id")

    if request.GET.get("active") == "1":
        qs = qs.filter(is_active=True)

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search) |
            Q(type__icontains=search)
        )

    qs = limit_queryset(request, qs)
    return Response(
        OrderReportSerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_order_report_detail(request, pk):
    try:
        obj = OrderReport.objects.get(pk=pk)
    except OrderReport.DoesNotExist:
        return Response({"detail": "Order report not found"}, status=404)

    return Response(OrderReportSerializer(obj, context={"request": request}).data)


def _check_captain_password(captain, raw_password):
    if hasattr(captain, "check_password"):
        return captain.check_password(raw_password)

    try:
        return check_password(raw_password, captain.password)
    except Exception:
        return captain.password == raw_password


def _get_captain_by_phone(phone):
    phone_text = str(phone).strip()
    digits = "".join(ch for ch in phone_text if ch.isdigit())

    candidates = [digits]

    if digits.startswith("0"):
        candidates.append(digits[1:])

    for item in candidates:
        if not item:
            continue

        try:
            return Captain.objects.get(phone=int(item))
        except Captain.DoesNotExist:
            continue
        except ValueError:
            continue

    return None


def _get_captain_from_token(request):
    auth_header = (
        request.META.get("HTTP_AUTHORIZATION")
        or request.headers.get("Authorization")
        or ""
    ).strip()

    token = ""

    if auth_header:
        parts = auth_header.split()

        if len(parts) == 2 and parts[0].lower() in ["token", "captaintoken"]:
            token = parts[1].strip()
        else:
            token = (
                auth_header
                .replace("CaptainToken", "")
                .replace("Token", "")
                .strip()
            )

    if not token:
        token = request.GET.get("token", "").strip()

    if not token:
        return None

    try:
        token_obj = CaptainToken.objects.select_related("user").get(key=token)
        return token_obj.user
    except CaptainToken.DoesNotExist:
        return None


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_captain_login(request):
    phone = request.data.get("phone")
    password = request.data.get("password")

    if not phone or not password:
        return Response(
            {"detail": "phone and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    captain = _get_captain_by_phone(phone)

    if captain is None:
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not _check_captain_password(captain, password):
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token_obj, created = CaptainToken.objects.get_or_create(
        user=captain,
        defaults={"key": secrets.token_hex(20)},
    )

    if not token_obj.key:
        token_obj.key = secrets.token_hex(20)
        token_obj.save()

    captain.is_logged = True
    captain.save(update_fields=["is_logged"])

    return Response({
        "token": token_obj.key,
        "captain": CaptainSerializer(captain, context={"request": request}).data,
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_captain_me(request):
    captain = _get_captain_from_token(request)

    if captain is None:
        return Response(
            {"detail": "Invalid or missing captain token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({
        "captain": CaptainSerializer(captain, context={"request": request}).data,
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_captain_orders(request):
    captain = _get_captain_from_token(request)

    if captain is None:
        return Response(
            {"detail": "Invalid or missing captain token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    qs = Order.objects.filter(captain=captain).order_by("-id")
    qs = limit_queryset(request, qs)

    return Response(
        OrderSerializer(qs, many=True, context={"request": request}).data
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_captain_accept_order(request, pk):
    captain = _get_captain_from_token(request)

    if captain is None:
        return Response(
            {"detail": "Invalid or missing captain token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        order = Order.objects.get(pk=pk, captain=captain)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Order not found for this captain"},
            status=status.HTTP_404_NOT_FOUND,
        )

    order.captain_status = "accepted"
    order.is_active = True
    order.save(update_fields=["captain_status", "is_active", "updated"])

    return Response({
        "detail": "Order accepted successfully",
        "order": OrderSerializer(order, context={"request": request}).data,
    })


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_captain_reject_order(request, pk):
    captain = _get_captain_from_token(request)

    if captain is None:
        return Response(
            {"detail": "Invalid or missing captain token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        order = Order.objects.get(pk=pk, captain=captain)
    except Order.DoesNotExist:
        return Response(
            {"detail": "Order not found for this captain"},
            status=status.HTTP_404_NOT_FOUND,
        )

    reason = request.data.get("reason", "رفض من الكابتن")

    order.captain_status = "rejected"
    order.rejection_reason = reason
    order.save(update_fields=["captain_status", "rejection_reason", "updated"])

    return Response({
        "detail": "Order rejected successfully",
        "order": OrderSerializer(order, context={"request": request}).data,
    })


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_captain_update_location(request):
    captain = _get_captain_from_token(request)

    if captain is None:
        return Response(
            {"detail": "Invalid or missing captain token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if latitude is None or longitude is None:
        return Response(
            {"detail": "latitude and longitude are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    captain.latitude = latitude
    captain.longitude = longitude
    captain.is_logged = True

    captain.save(
        update_fields=[
            "latitude",
            "longitude",
            "is_logged",
            "updated",
        ]
    )

    return Response({
        "detail": "Captain location updated successfully",
        "captain": CaptainSerializer(captain, context={"request": request}).data,
    })
    
    MANDOB_TOKEN_SALT = "mandob-mobile-token"


def _make_mandob_token(mandob):
    return signing.dumps(
        {
            "type": "mandob",
            "id": mandob.id,
        },
        salt=MANDOB_TOKEN_SALT,
    )


def _check_mandob_password(mandob, raw_password):
    stored_password = str(getattr(mandob, "password", "") or "")

    if hasattr(mandob, "check_password"):
        try:
            if mandob.check_password(raw_password):
                return True
        except Exception:
            pass

    try:
        if check_password(raw_password, stored_password):
            return True
    except Exception:
        pass

    return stored_password == str(raw_password)


def _get_mandob_by_phone(phone):
    phone_text = str(phone).strip()
    digits = "".join(ch for ch in phone_text if ch.isdigit())

    candidates = [digits]

    if digits.startswith("0"):
        candidates.append(digits[1:])

    for item in candidates:
        if not item:
            continue

        try:
            return Mandob.objects.get(phone=int(item))
        except Mandob.DoesNotExist:
            continue
        except ValueError:
            continue

        try:
            return Mandob.objects.get(phone=item)
        except Mandob.DoesNotExist:
            continue

    return None


def _get_mandob_from_token(request):
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
            "mandobtoken",
        ]:
            token = parts[1].strip()
        else:
            token = (
                auth_header
                .replace("MandobToken", "")
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
            salt=MANDOB_TOKEN_SALT,
            max_age=60 * 60 * 24 * 365,
        )

        if data.get("type") != "mandob":
            return None

        return Mandob.objects.get(pk=data.get("id"))

    except Exception:
        return None


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_mandob_login(request):
    phone = request.data.get("phone")
    password = request.data.get("password")

    if not phone or not password:
        return Response(
            {"detail": "phone and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    mandob = _get_mandob_by_phone(phone)

    if mandob is None:
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not _check_mandob_password(mandob, password):
        return Response(
            {"detail": "Invalid phone or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if hasattr(mandob, "is_logged"):
        mandob.is_logged = True
        try:
            mandob.save(update_fields=["is_logged"])
        except Exception:
            mandob.save()

    token = _make_mandob_token(mandob)

    return Response({
        "id": mandob.id,
        "token": token,
        "mandob": MandobSerializer(
            mandob,
            context={"request": request},
        ).data,
    })


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_mandob_me(request):
    mandob = _get_mandob_from_token(request)

    if mandob is None:
        return Response(
            {"detail": "Invalid or missing mandob token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({
        "mandob": MandobSerializer(
            mandob,
            context={"request": request},
        ).data,
    })


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_mandob_update_location(request):
    mandob = _get_mandob_from_token(request)

    if mandob is None:
        return Response(
            {"detail": "Invalid or missing mandob token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if latitude is None or longitude is None:
        return Response(
            {"detail": "latitude and longitude are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    mandob.latitude = latitude
    mandob.longitude = longitude

    if hasattr(mandob, "is_logged"):
        mandob.is_logged = True

    update_fields = ["latitude", "longitude"]

    if hasattr(mandob, "is_logged"):
        update_fields.append("is_logged")

    if hasattr(mandob, "updated"):
        update_fields.append("updated")

    try:
        mandob.save(update_fields=update_fields)
    except Exception:
        mandob.save()

    return Response({
        "detail": "Mandob location updated successfully",
        "mandob": MandobSerializer(
            mandob,
            context={"request": request},
        ).data,
    })


@api_view(["GET", "PATCH"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_mandob_mobile_detail(request, pk):
    try:
        mandob = Mandob.objects.get(pk=pk)
    except Mandob.DoesNotExist:
        return Response(
            {"detail": "Mandob not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        return Response(
            MandobSerializer(
                mandob,
                context={"request": request},
            ).data
        )

    allowed_fields = [
        "is_logged",
        "isfree",
        "latitude",
        "longitude",
        "latitude2",
        "longitude2",
        "location",
        "city",
    ]

    changed_fields = []

    for field in allowed_fields:
        if field in request.data and hasattr(mandob, field):
            setattr(mandob, field, request.data.get(field))
            changed_fields.append(field)

    if hasattr(mandob, "updated"):
        changed_fields.append("updated")

    if changed_fields:
        try:
            mandob.save(update_fields=changed_fields)
        except Exception:
            mandob.save()

    return Response(
        MandobSerializer(
            mandob,
            context={"request": request},
        ).data
    )
    