from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import province_filter
from ..forms import *
from home.generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_province(CreateView):
    model = Province
    template_name = "create_province.html"
    success_url = "/list_province"
    form_class = province_form


@method_decorator(login_required(), name="dispatch")
class list_province(filter_view_generic):
    queryset = Province.objects.all().order_by('-id')
    model = Province
    template_name = "list_province.html"
    paginate_by = 25
    filterset_class = province_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_province(UpdateView):
    model = Province
    template_name = "update_province.html"
    success_url = "/list_province"
    form_class = province_form


@method_decorator(login_required(), name="dispatch")
class delete_province(DeleteView):
    model = Province
    template_name = "delete.html"
    success_url = "/list_province"
