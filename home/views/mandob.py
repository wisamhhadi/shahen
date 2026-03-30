from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import mandob_filter, report_filter, order_report_filter, history_filter
from ..forms import *
from home.generics import filter_view_generic
from mandob.models import Mandob, OrderReportItem, Room, History, Attendance
from django.utils import timezone
from django.db.models import Count, Max
from datetime import date

@method_decorator(login_required(), name="dispatch")
class create_mandob(CreateView):
    model = Mandob
    template_name = "create_mandob.html"
    success_url = "/list_mandob"
    form_class = mandob_form


@method_decorator(login_required(), name="dispatch")
class list_mandob(filter_view_generic):
    queryset = Mandob.objects.all().order_by('-id')
    model = Mandob
    template_name = "list_mandob.html"
    paginate_by = 25
    filterset_class = mandob_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_mandob(UpdateView):
    model = Mandob
    template_name = "update_mandob.html"
    success_url = "/list_mandob"
    form_class = mandob_form_update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mandob_obj = self.object
        context['attendance_objects'] = Attendance.objects.filter(mandob=mandob_obj).order_by('-id')[:20]
        context['history_objects'] = History.objects.filter(mandob=mandob_obj).order_by('-id')[:20]
        return context


@method_decorator(login_required(), name="dispatch")
class delete_mandob(DeleteView):
    model = Mandob
    template_name = "delete.html"
    success_url = "/list_mandob"


@login_required()
def day_mandob_question_view(request):
    objects = Question.objects.all().filter(type='day').order_by('-id')
    form_set = modelformset_factory(Question, form=mandob_question_form, extra=18, can_delete=True,
                                    can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.type = "day"
                form.save()
        return redirect('day_mandob_question_view')

    ctx = {
        'forms': form_set2,
    }

    return render(request, "questions/question_day.html", ctx)


@login_required()
def week_mandob_question_view(request):
    objects = Question.objects.all().filter(type='week').order_by('-id')
    form_set = modelformset_factory(Question, form=mandob_question_form, extra=18, can_delete=True,
                                    can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.type = "week"
                form.save()
        return redirect('week_mandob_question_view')

    ctx = {
        'forms': form_set2,
    }

    return render(request, "questions/question_week.html", ctx)


@login_required()
def month_mandob_question_view(request):
    objects = Question.objects.all().filter(type='month').order_by('-id')
    form_set = modelformset_factory(Question, form=mandob_question_form, extra=18, can_delete=True,
                                    can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.type = "month"
                form.save()
        return redirect('month_mandob_question_view')

    ctx = {
        'forms': form_set2,
    }

    return render(request, "questions/question_month.html", ctx)


@login_required()
def year_mandob_question_view(request):
    objects = Question.objects.all().filter(type='year').order_by('-id')
    form_set = modelformset_factory(Question, form=mandob_question_form, extra=18, can_delete=True,
                                    can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.type = "year"
                form.save()
        return redirect('year_mandob_question_view')

    ctx = {
        'forms': form_set2,
    }

    return render(request, "questions/question_year.html", ctx)


@login_required()
def custom_mandob_question_view(request):

    ctx = {
        # 'forms': form_set2,
    }

    return render(request, "create_custom_report.html", ctx)


@method_decorator(login_required(), name="dispatch")
class list_report(filter_view_generic):
    queryset = Report.objects.all().order_by('-id')
    model = Report
    template_name = "list_report.html"
    paginate_by = 25
    filterset_class = report_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_report(UpdateView):
    model = Report
    template_name = "update_report.html"
    success_url = "/list_report"
    form_class = report_form

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data()
        context['parameters'] = parameters
        context['answers'] = Answer.objects.all().filter(report=self.object).order_by('-id')
        return context


@method_decorator(login_required(), name="dispatch")
class delete_report(DeleteView):
    model = Report
    template_name = "delete.html"
    success_url = "/list_report"


@method_decorator(login_required(), name="dispatch")
class list_order_report(filter_view_generic):
    queryset = OrderReport.objects.all().order_by('-id')
    model = OrderReport
    template_name = "list_order_report.html"
    paginate_by = 25
    filterset_class = order_report_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_order_report(UpdateView):
    model = OrderReport
    template_name = "update_order_report.html"
    success_url = "/list_order_report"
    form_class = order_report_form

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data()
        context['parameters'] = parameters
        context['items'] = OrderReportItem.objects.all().filter(order=self.object).order_by('-id')
        return context


@method_decorator(login_required(), name="dispatch")
class delete_order_report(DeleteView):
    model = OrderReport
    template_name = "delete.html"
    success_url = "/list_order_report"


@login_required
def chat_room(request, mandob_id):
    """
    Chat room view for communicating with a specific mandob
    """
    mandob = get_object_or_404(Mandob, id=mandob_id, is_active=True)
    print(Room.objects.all().filter(room=mandob))
    if Room.objects.all().filter(room=mandob).exists() is False:
        Room.objects.create(room=mandob,is_active=True)

    context = {
        'mandob': mandob,
        'page_title': f'محادثة مع {mandob.name}',
    }

    return render(request, 'chat.html', context)


@method_decorator(login_required(), name="dispatch")
class list_history(filter_view_generic):
    queryset = History.objects.all().order_by('-id')
    model = History
    template_name = "list_history.html"
    paginate_by = 25
    filterset_class = history_filter
    context_object_name = "objects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate statistics
        queryset = self.get_queryset()
        today = timezone.now().date()

        # Basic stats
        total_records = queryset.count()
        active_records = queryset.filter(is_active=True).count()
        today_records = queryset.filter(created__date=today).count()
        total_mandobs = queryset.values('mandob').distinct().count()

        # Type distribution
        type_stats = queryset.values('type').annotate(count=Count('type'))
        captain_count = next((item['count'] for item in type_stats if item['type'] == 'captain'), 0)
        user_count = next((item['count'] for item in type_stats if item['type'] == 'user'), 0)
        company_count = next((item['count'] for item in type_stats if item['type'] == 'company'), 0)
        deliverycompany_count = next((item['count'] for item in type_stats if item['type'] == 'deliverycompany'), 0)
        car_count = next((item['count'] for item in type_stats if item['type'] == 'car'), 0)

        # Top mandobs by activity
        top_mandobs = (queryset.values('mandob', 'mandob__name')
                       .annotate(
            record_count=Count('id'),
            latest_activity=Max('updated')
        )
                       .order_by('-record_count')[:5])

        stats = {
            'total_records': total_records,
            'active_records': active_records,
            'today_records': today_records,
            'total_mandobs': total_mandobs,
            'captain_count': captain_count,
            'user_count': user_count,
            'company_count': company_count,
            'deliverycompany_count': deliverycompany_count,
            'car_count': car_count,
            'top_mandobs': top_mandobs,
        }

        context['stats'] = stats
        return context