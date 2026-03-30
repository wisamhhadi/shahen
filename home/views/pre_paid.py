from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView,ListView
from ..forms import *
from ..filters import pre_paid_filter
from ..generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_pre_paid(CreateView):
    model = PrePaid
    template_name = "create_pre_paid.html"
    success_url = "/list_pre_paid"
    form_class = pre_paid_form


@method_decorator(login_required(), name="dispatch")
class list_pre_paid(filter_view_generic):
    queryset = PrePaid.objects.all().order_by('-id')
    model = PrePaid
    template_name = "list_pre_paid.html"
    paginate_by = 25
    filterset_class = pre_paid_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_pre_paid(UpdateView):
    model = PrePaid
    template_name = "update_pre_paid.html"
    success_url = "/list_pre_paid"
    form_class = pre_paid_form


@method_decorator(login_required(), name="dispatch")
class delete_pre_paid(DeleteView):
    model = PrePaid
    template_name = "delete.html"
    success_url = "/list_pre_paid"
