from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse

from captain.models import Captain
from mandob.models import Mandob
from order.models import Order


def mandob_map(request):
    return render(request, 'mandob_map.html')

@login_required
def mandob_autocomplete_map(request):
    try:
        if request.user.is_staff:
            mandobs = Mandob.objects.select_related(
                'country', 'province', 'admin'
            ).filter(admin=request.user)

        else:
            mandobs = Mandob.objects.select_related(
                'country', 'province', 'admin'
            )

        mandobs_data = []
        for mandob in mandobs:
            mandobs_data.append({
                'id': mandob.id,
                'name': mandob.name,
                'phone': mandob.phone,
                'latitude': mandob.latitude,
                'longitude': float(mandob.longitude) if mandob.longitude else None,
                'radius': mandob.radius or 500,
                'latitude2': float(mandob.latitude2) if hasattr(mandob, 'latitude2') and mandob.latitude2 else None,
                'longitude2': float(mandob.longitude2) if hasattr(mandob, 'longitude2') and mandob.longitude2 else None,
                'city': f"{mandob.country.name if mandob.country else ''} - {mandob.city or ''}".strip(' -'),
                'is_active': mandob.is_active,
                'last_seen': get_last_seen_text(mandob),
            })

        return JsonResponse({'results': mandobs_data})
    except Exception as e:
        return JsonResponse({'error': str(e), 'results': []})


def captain_map(request):
    return render(request, 'captain_map.html')


@login_required
def captain_autocomplete_map(request):
    """
    API endpoint for captains data with location info
    """
    try:
        captains = Captain.objects.filter(is_active=True).select_related(
            'country', 'province'
        )

        captains_data = []
        for captain in captains:
            # Get captain's vehicle info
            vehicle_info = get_captain_vehicle_info(captain)

            captains_data.append({
                'id': captain.id,
                'name': captain.name,
                'phone': captain.phone,
                'latitude': float(captain.latitude) if hasattr(captain, 'latitude') and captain.latitude else None,
                'longitude': float(captain.longitude) if hasattr(captain, 'longitude') and captain.longitude else None,
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
        return JsonResponse({'error': str(e), 'results': []})


def get_captain_vehicle_info(captain):
    """
    Get captain's vehicle information
    """
    try:
        # Assuming captain has a related car
        if hasattr(captain, 'car') and captain.car:
            car = captain.car
            vehicle = f"{car.company.name if car.company else ''} {car.model.name if car.model else ''} {car.year or ''}".strip()
            plate_number = f"{car.province.name if car.province else ''} {car.number or ''}".strip()
        else:
            vehicle = "غير محدد"
            plate_number = "غير محدد"

        return {
            'vehicle': vehicle,
            'plate_number': plate_number
        }
    except:
        return {
            'vehicle': "غير محدد",
            'plate_number': "غير محدد"
        }


def get_captain_status(captain):
    """
    Determine captain's current status
    """
    try:
        # You can implement logic to determine status based on:
        # - Active orders
        # - Last location update
        # - Manual status setting

        # For now, return a sample status
        if not captain.is_active:
            return 'offline'

        # Check if captain has active orders
        if get_captain_current_order(captain):
            return 'driving'

        # Check if recently updated location (last 30 minutes)
        if hasattr(captain, 'updated') and captain.updated:
            if captain.updated > timezone.now() - timedelta(minutes=30):
                return 'online'

        return 'offline'
    except:
        return 'offline'


def get_captain_current_order(captain):
    """
    Get captain's current active order if any
    """
    try:
        # Assuming orders have a captain field and status
        active_order = Order.objects.filter(
            captain=captain,
            status__in=['in_progress', 'picked_up']  # Adjust status values as needed
        ).first()

        if active_order:
            return f"شحنة #{active_order.id}"
        return None
    except:
        return None


def get_last_seen_text(obj):
    """
    Get human-readable last seen text
    """
    try:
        if hasattr(obj, 'updatedtime') and obj.updatedtime:
            diff = timezone.now() - obj.updated

            if diff.seconds < 60:
                return "الآن"
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} دقيقة"
            elif diff.seconds < 86400:
                hours = diff.seconds // 3600
                return f"{hours} ساعة"
            else:
                days = diff.days
                return f"{days} يوم"

        return "غير معروف"
    except:
        return "غير معروف"