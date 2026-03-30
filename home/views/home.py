from ..forms import *
from django.contrib import messages
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout, login
from django.shortcuts import redirect, reverse, render
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Import your models
from core.models import *
from user.models import User
from deliverycompany.models import DeliveryCompany
from captain.models import Captain
from mandob.models import Mandob, Attendance
from order.models import Order, OrderCar, OrderOffer


@login_required()
def index(request):
    stats = {
        # Basic counts
        'products_count': get_products_count(),
        'users_count': User.objects.filter(is_active=True).count(),
        'merchants_count': get_merchants_count(),
        'carriers_count': DeliveryCompany.objects.filter(is_active=True).count(),

        # Mandobs statistics
        'active_mandobs_count': Mandob.objects.filter(is_active=True).count(),
        'inactive_mandobs_count': Mandob.objects.filter(is_active=False).count(),
        'total_mandobs_count': Mandob.objects.count(),
        'inside_range_count': get_mandobs_inside_range(),
        'outside_range_count': get_mandobs_outside_range(),

        # Drivers/Captains statistics
        'drivers_count': Captain.objects.filter(is_active=True).count(),

        # Orders/Shipments statistics
        'shipments_count': Order.objects.count(),
        'total_shipments': Order.objects.count(),

        # Management
        'managers_count': Admin.objects.filter(is_active=True).count(),

        # Vehicles statistics
        'monthly_vehicles_count': get_monthly_vehicles_count(),
        'daily_vehicles_count': get_daily_vehicles_count(),
    }

    # Get recent activity
    recent_mandobs = Mandob.objects.filter(
        created__gte=timezone.now() - timedelta(days=7)
    ).order_by('-created')[:5]

    recent_orders = Order.objects.filter(
        created__gte=timezone.now() - timedelta(days=7)
    ).order_by('-created')[:5]

    context = {
        'stats': stats,
        'recent_mandobs': recent_mandobs,
        'recent_orders': recent_orders,
    }

    return render(request, 'index.html',context)


@method_decorator(login_required(), name="dispatch")
class update_info(UpdateView):
    model = Info
    template_name = "update_info.html"
    success_url = "/"
    form_class = info_form


@method_decorator(login_required(), name="dispatch")
class profile(UpdateView):
    model = Admin
    template_name = "update_admin.html"
    form_class = admin_form_update
    success_url = "/"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.user.id
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


def logout_page(request):
    logout(request)
    return redirect(reverse('login'))


def login_page(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        if phone is None or password is None:
            messages.add_message(request=request, level=messages.WARNING, message="خطآ في رقم الهاتف او الرمز السري")
            return redirect(reverse("login"))

        admin = Admin.objects.all().filter(phone=phone).exists()
        if admin:
            admin = Admin.objects.get(phone=phone)
            if admin.check_password(password):
                if(admin.is_staff) :
                    login(request, admin)
                    return redirect(reverse("list_mandob"))
                else:
                    login(request, admin)
                    return redirect(reverse("home"))
            else:
                messages.add_message(request=request, level=messages.WARNING,
                                     message="خطآ في رقم الهاتف او الرمز السري")
                return redirect(reverse("login"))
        else:
            messages.add_message(request=request, level=messages.WARNING, message="خطآ في رقم الهاتف او الرمز السري")
            return redirect(reverse("login"))

    return render(request, 'login.html')


def get_products_count():
    """
    Calculate products count - adjust based on your product model
    """
    try:
        # If you have a Product model, use: Product.objects.count()
        # For now, return 0 or calculate from other models
        return 0
    except:
        return 0


def get_merchants_count():
    """
    Calculate merchants count - users with merchant role
    """
    try:
        return User.objects.filter(
            user_type='merchant',  # Adjust field name as needed
            is_active=True
        ).count()
    except:
        # Alternative: count delivery companies as merchants
        return DeliveryCompany.objects.filter(is_active=True).count()


def get_mandobs_inside_range():
    """
    Calculate mandobs currently inside their assigned range
    This would require real-time location data
    """
    try:
        # You would need to implement the logic to check if mandob's
        # current location (lat2, long2) is within their radius
        # For now, return a sample calculation
        total_mandobs = Mandob.objects.filter(is_active=True).count()
        return int(total_mandobs * 0.7)  # Assume 70% are inside range
    except:
        return 0


def get_mandobs_outside_range():
    """
    Calculate mandobs currently outside their assigned range
    """
    try:
        total_active = Mandob.objects.filter(is_active=True).count()
        inside_range = get_mandobs_inside_range()
        return total_active - inside_range
    except:
        return 0


def get_monthly_vehicles_count():
    """
    Get vehicles registered this month
    """
    try:
        start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return Car.objects.filter(
            created__gte=start_of_month
        ).count()
    except:
        return 0


def get_daily_vehicles_count():
    """
    Get vehicles registered today
    """
    try:
        today = timezone.now().date()
        return Car.objects.filter(
            created__date=today
        ).count()
    except:
        return 0