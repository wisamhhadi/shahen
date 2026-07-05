import json
import os

from django.core import signing
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from captain.models import Captain
from deliverycompany.models import DeliveryCompany

TRANSPORTER_TOKEN_SALT = "transporter-mobile-token"


def _model_has_field(model, field_name):
    try:
        model._meta.get_field(field_name)
        return True
    except Exception:
        return False


def _get_transporter_from_token(request):
    header = (request.META.get("HTTP_AUTHORIZATION") or request.headers.get("Authorization") or "").strip()
    token = ""
    if header:
        parts = header.split()
        if len(parts) == 2 and parts[0].lower() in ["bearer", "token"]:
            token = parts[1].strip()
        else:
            token = header.replace("Bearer", "").replace("Token", "").strip()
    if not token:
        token = request.data.get("token") or request.GET.get("token") or ""
    if not token:
        return None
    try:
        data = signing.loads(token, salt=TRANSPORTER_TOKEN_SALT, max_age=60 * 60 * 24 * 365)
        if data.get("type") != "transporter":
            return None
        return DeliveryCompany.objects.get(pk=data.get("id"))
    except Exception:
        return None


def _save_device_token(obj, fcm_token):
    if not fcm_token:
        return False
    if _model_has_field(obj.__class__, "fcm_token"):
        obj.fcm_token = fcm_token
        obj.save(update_fields=["fcm_token"])
        return True
    if _model_has_field(obj.__class__, "device_id"):
        obj.device_id = fcm_token
        obj.save(update_fields=["device_id"])
        return True
    return False


def _get_device_token(obj):
    if obj is None:
        return None
    if hasattr(obj, "fcm_token") and getattr(obj, "fcm_token", None):
        return getattr(obj, "fcm_token")
    if hasattr(obj, "device_id") and getattr(obj, "device_id", None):
        return getattr(obj, "device_id")
    return None


def _firebase_messaging():
    try:
        import firebase_admin
        from firebase_admin import credentials, messaging
    except Exception as exc:
        return None, f"firebase-admin غير مثبت: {exc}"
    try:
        if not firebase_admin._apps:
            credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON", "").strip()
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
            if credentials_json:
                cred = credentials.Certificate(json.loads(credentials_json))
            elif credentials_path:
                cred = credentials.Certificate(credentials_path)
            else:
                return None, "لم يتم ضبط FIREBASE_CREDENTIALS_JSON أو GOOGLE_APPLICATION_CREDENTIALS"
            firebase_admin.initialize_app(cred)
        return messaging, None
    except Exception as exc:
        return None, f"فشل تهيئة Firebase Admin: {exc}"


def send_push_to_token(fcm_token, title, body, data=None):
    messaging, error = _firebase_messaging()
    if error:
        return False, error
    if not fcm_token:
        return False, "لا يوجد FCM token للمستخدم"
    try:
        message = messaging.Message(
            token=fcm_token,
            notification=messaging.Notification(title=str(title or "شحنكو"), body=str(body or "")),
            data={str(k): str(v) for k, v in (data or {}).items()},
        )
        message_id = messaging.send(message)
        return True, message_id
    except Exception as exc:
        return False, str(exc)


def send_push_to_transporter(transporter, title, body, data=None):
    return send_push_to_token(_get_device_token(transporter), title, body, data)


def send_push_to_captain(captain, title, body, data=None):
    return send_push_to_token(_get_device_token(captain), title, body, data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_register_fcm_token(request):
    transporter = _get_transporter_from_token(request)
    if transporter is None:
        return Response({"detail": "Invalid or missing transporter token"}, status=status.HTTP_401_UNAUTHORIZED)
    fcm_token = request.data.get("fcm_token") or request.data.get("device_token") or request.data.get("device_id")
    if not fcm_token:
        return Response({"detail": "fcm_token is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not _save_device_token(transporter, fcm_token):
        return Response({"detail": "لا يوجد حقل device_id أو fcm_token في موديل الناقل"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "تم حفظ رمز الإشعارات للناقل", "transporter_id": transporter.id, "token_saved": True})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def transporter_send_test_notification(request):
    transporter = _get_transporter_from_token(request)
    if transporter is None:
        return Response({"detail": "Invalid or missing transporter token"}, status=status.HTTP_401_UNAUTHORIZED)
    ok, result = send_push_to_transporter(
        transporter,
        request.data.get("title") or "شحنكو",
        request.data.get("body") or "تم تفعيل إشعارات تطبيق الناقلين بنجاح",
        data={"type": "test", "target": "transporter", "id": transporter.id},
    )
    return Response({"sent": ok, "result": result, "transporter_id": transporter.id}, status=status.HTTP_200_OK if ok else status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def send_test_to_captain_by_id(request):
    captain_id = request.data.get("captain_id")
    if not captain_id:
        return Response({"detail": "captain_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        captain = Captain.objects.get(pk=captain_id)
    except Captain.DoesNotExist:
        return Response({"detail": "Captain not found"}, status=status.HTTP_404_NOT_FOUND)
    ok, result = send_push_to_captain(
        captain,
        request.data.get("title") or "شحنكو",
        request.data.get("body") or "إشعار تجريبي للسائق",
        data={"type": "test", "target": "captain", "id": captain.id},
    )
    return Response({"sent": ok, "result": result, "captain_id": captain.id}, status=status.HTTP_200_OK if ok else status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def notifications_health(request):
    messaging, error = _firebase_messaging()
    return Response({"firebase_ready": error is None, "error": error})
