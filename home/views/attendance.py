from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count, Q , FloatField, DecimalField
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic import CreateView

from home.filters import attendance_filter
from home.forms import attendance_form
from home.generics import filter_view_generic
from mandob.models import Attendance


@method_decorator(login_required(), name="dispatch")
class create_attendance(CreateView):
    model = Attendance
    template_name = "create_attendance.html"
    success_url = "/list_attendance"
    form_class = attendance_form


@method_decorator(login_required(), name="dispatch")
class list_attendance(filter_view_generic):
    queryset = Attendance.objects.all().order_by('-id')
    model = Attendance
    template_name = "list_attendance.html"
    paginate_by = 25
    filterset_class = attendance_filter
    context_object_name = "objects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the filtered queryset (same as what's being displayed)
        filtered_queryset = self.get_queryset()
        if hasattr(self, 'filterset') and self.filterset:
            filtered_queryset = self.filterset.qs

        # Calculate statistics based on filtered data
        stats = self.calculate_statistics(filtered_queryset)
        context.update(stats)

        return context

    def calculate_statistics(self, queryset):
        """Calculate attendance statistics"""

        # Basic counts
        total_records = queryset.count()
        total_employees = queryset.values('mandob').distinct().count()

        # Working hours statistics
        work_hours_stats = queryset.aggregate(
            total_work_hours=Coalesce(Sum('work_hour', output_field=FloatField()), 0.0, output_field=FloatField()),
            avg_work_hours=Coalesce(Avg('work_hour', output_field=FloatField()), 0.0, output_field=FloatField()),
        )

        # Present/Absent counts (assuming null leave_time means still working or absent)
        present_count = queryset.filter(
            attend_time__isnull=False,
            leave_time__isnull=False
        ).count()

        incomplete_attendance = queryset.filter(
            attend_time__isnull=False,
            leave_time__isnull=True
        ).count()

        absent_count = total_records - present_count - incomplete_attendance

        # Today's statistics
        today = timezone.now().date()
        today_stats = queryset.filter(day=today).aggregate(
            today_total=Count('id'),
            today_work_hours=Coalesce(Sum('work_hour', output_field=FloatField()), 0.0, output_field=FloatField()),
            today_present=Count('id', filter=Q(attend_time__isnull=False, leave_time__isnull=False)),
        )

        # This week's statistics
        week_start = today - timedelta(days=today.weekday())
        week_stats = queryset.filter(day__gte=week_start).aggregate(
            week_total=Count('id'),
            week_work_hours=Coalesce(Sum('work_hour', output_field=FloatField()), 0.0, output_field=FloatField()),
        )

        # This month's statistics
        month_start = today.replace(day=1)
        month_stats = queryset.filter(day__gte=month_start).aggregate(
            month_total=Count('id'),
            month_work_hours=Coalesce(Sum('work_hour', output_field=FloatField()), 0.0, output_field=FloatField()),
        )

        # Top performing employees (by total work hours)
        top_employees = queryset.values('mandob__name').annotate(
            total_hours=Sum('work_hour', output_field=FloatField()),
            attendance_count=Count('id')
        ).order_by('-total_hours')[:5]

        # Daily attendance trend (last 7 days)
        daily_trend = []
        for i in range(7):
            date = today - timedelta(days=i)
            daily_count = queryset.filter(day=date).count()
            daily_hours = queryset.filter(day=date).aggregate(
                total_hours=Coalesce(Sum('work_hour', output_field=FloatField()), 0.0, output_field=FloatField())
            )['total_hours']
            daily_trend.append({
                'date': date,
                'count': daily_count,
                'hours': float(daily_hours) if daily_hours else 0.0
            })

        return {
            'stats': {
                'total_records': total_records,
                'total_employees': total_employees,
                'total_work_hours': float(work_hours_stats['total_work_hours']),
                'avg_work_hours': round(float(work_hours_stats['avg_work_hours']), 2),
                'present_count': present_count,
                'incomplete_attendance': incomplete_attendance,
                'absent_count': absent_count,
                'today_total': today_stats['today_total'],
                'today_work_hours': float(today_stats['today_work_hours']),
                'today_present': today_stats['today_present'],
                'week_total': week_stats['week_total'],
                'week_work_hours': float(week_stats['week_work_hours']),
                'month_total': month_stats['month_total'],
                'month_work_hours': float(month_stats['month_work_hours']),
                'top_employees': top_employees,
                'daily_trend': daily_trend,
            }
        }


