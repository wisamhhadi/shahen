import secrets

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
    