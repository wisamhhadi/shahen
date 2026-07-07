from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

from captain.models import Captain
from mandob.models import Mandob
from order.models import Order


@login_required
def mandob_map(request):
    return render(request, 'mandob_map.html')


@login_required
def mandob_autocomplete_map(request):
    """
    API endpoint for mandobs data with zone and current location info.
    المدير العام يرى كل المندوبين.
    مسؤول المندوبين يرى المندوبين المرتبطين به إذا كانوا موجودين.
    """
    try:
        def to_float(value):
            if value is None or value == "":
                return None
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        mandobs = Mandob.objects.select_related(
            'country',
            'province',
            'admin',
        ).filter(is_active=True)

        # المشكلة القديمة:
        # إذا كان Admin عنده is_staff=True كان النظام يفلتر admin=request.user
        # فيظهر صفر للمندوبين إذا لم يكونوا مربوطين مباشرة بهذا المدير.
        if not request.user.is_superuser and request.user.is_staff:
            assigned_mandobs = mandobs.filter(admin=request.user)

            # إذا توجد مندوبين مربوطين بهذا المسؤول، نعرضهم فقط.
            # إذا لا توجد، نترك القائمة العامة حتى لا تظهر الصفحة فارغة للمدير العام/الإداري.
            if assigned_mandobs.exists():
                mandobs = assigned_mandobs

        mandobs_data = []

        for mandob in mandobs:
            mandobs_data.append({
                'id': mandob.id,
                'name': mandob.name or '',
                'phone': str(mandob.phone) if mandob.phone else '',
                'latitude': to_float(mandob.latitude),
                'longitude': to_float(mandob.longitude),
                'radius': mandob.radius or 500,
                'latitude2': to_float(getattr(mandob, 'latitude2', None)),
                'longitude2': to_float(getattr(mandob, 'longitude2', None)),
                'city': f"{mandob.country.name if mandob.country else ''} - {mandob.city or ''}".strip(' -'),
                'is_active': mandob.is_active,
                'last_seen': get_last_seen_text(mandob),
            })

        return JsonResponse({'results': mandobs_data})

    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'results': [],
        })


@login_required
def captain_map(request):
    return render(request, 'captain_map.html')


@login_required
def captain_autocomplete_map(request):
    """
    API endpoint for captains data with location info.
    """
    try:
        captains = Captain.objects.filter(is_active=True).select_related(
            'country',
            'province',
        )

        captains_data = []

        for captain in captains:
            vehicle_info = get_captain_vehicle_info(captain)

            captains_data.append({
                'id': captain.id,
                'name': captain.name or '',
                'phone': str(captain.phone) if captain.phone else '',
                'latitude': safe_float(getattr(captain, 'latitude', None)),
                'longitude': safe_float(getattr(captain, 'longitude', None)),
                'city': f"{captain.country.name if captain.country else ''} - {captain.city or ''}".strip(' -'),
                'vehicle': vehicle_info['vehicle'],
                'plate_number': vehicle_info['plate_number'],
                'status': get_captain_status(captain),
                'is_active': captain.is_active,
                'last_seen': get_last_seen_text(captain),
                'current_order': get_captain_current_order(captain),
            })

        return JsonResponse({'results': captains_data})

    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'results': [],
        })


def safe_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_captain_vehicle_info(captain):
    """
    Get captain's vehicle information.
    """
    try:
        if hasattr(captain, 'car') and captain.car:
            car = captain.car

            vehicle_parts = []

            if hasattr(car, 'car_company') and car.car_company:
                vehicle_parts.append(str(car.car_company))

            if hasattr(car, 'car_model') and car.car_model:
                vehicle_parts.append(str(car.car_model))

            if hasattr(car, 'car_manu_year') and car.car_manu_year:
                vehicle_parts.append(str(car.car_manu_year))

            vehicle = " ".join(vehicle_parts).strip() or "غير محدد"

            plate_parts = []

            if hasattr(car, 'province') and car.province:
                plate_parts.append(str(car.province))

            if hasattr(car, 'car_number') and car.car_number:
                plate_parts.append(str(car.car_number))

            if hasattr(car, 'car_letter') and car.car_letter:
                plate_parts.append(str(car.car_letter))

            plate_number = " ".join(plate_parts).strip() or "غير محدد"

        else:
            vehicle = "غير محدد"
            plate_number = "غير محدد"

        return {
            'vehicle': vehicle,
            'plate_number': plate_number,
        }

    except Exception:
        return {
            'vehicle': "غير محدد",
            'plate_number': "غير محدد",
        }


def get_captain_status(captain):
    """
    Determine captain's current status.
    """
    try:
        if not captain.is_active:
            return 'offline'

        if get_captain_current_order(captain):
            return 'driving'

        last_time = getattr(captain, 'updatedtime', None) or getattr(captain, 'updated', None)

        if last_time and last_time > timezone.now() - timedelta(minutes=30):
            return 'online'

        return 'offline'

    except Exception:
        return 'offline'


def get_captain_current_order(captain):
    """
    Get captain's current active order if any.
    """
    try:
        active_order = Order.objects.filter(
            captain=captain,
            status__in=['in_progress', 'picked_up']
        ).first()

        if active_order:
            return f"شحنة #{active_order.id}"

        return None

    except Exception:
        return None


def get_last_seen_text(obj):
    """
    Get human-readable last seen text.
    """
    try:
        last_time = getattr(obj, 'updatedtime', None) or getattr(obj, 'updated', None)

        if not last_time:
            return "غير معروف"

        diff = timezone.now() - last_time
        seconds = diff.total_seconds()

        if seconds < 60:
            return "الآن"

        if seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} دقيقة"

        if seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} ساعة"

        return f"{diff.days} يوم"

    except Exception:
        return "غير معروف"