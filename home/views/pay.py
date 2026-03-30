from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import pay_filter
from ..forms import *
from home.generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_pay(CreateView):
    model = Pay
    template_name = "create_pay.html"
    success_url = "/list_pay"
    form_class = pay_form


@method_decorator(login_required(), name="dispatch")
class list_pay(filter_view_generic):
    queryset = Pay.objects.all().order_by('-id')
    model = Pay
    template_name = "list_pay.html"
    paginate_by = 25
    filterset_class = pay_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_pay(UpdateView):
    model = Pay
    template_name = "update_pay.html"
    success_url = "/list_pay"
    form_class = pay_form


@method_decorator(login_required(), name="dispatch")
class delete_pay(DeleteView):
    model = Pay
    template_name = "delete.html"
    success_url = "/list_pay"
