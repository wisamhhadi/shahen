from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import delivery_company_filter
from home.forms import *
from home.generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_delivery_company(CreateView):
    model = DeliveryCompany
    template_name = "create_delivery_company.html"
    success_url = "/list_delivery_company"
    form_class = delivery_company_form


@method_decorator(login_required(), name="dispatch")
class list_delivery_company(filter_view_generic):
    queryset = DeliveryCompany.objects.all().order_by('-id')
    model = DeliveryCompany
    template_name = "list_delivery_company.html"
    paginate_by = 25
    filterset_class = delivery_company_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_delivery_company(UpdateView):
    model = DeliveryCompany
    template_name = "update_delivery_company.html"
    success_url = "/list_delivery_company"
    form_class = delivery_company_form_update


@method_decorator(login_required(), name="dispatch")
class delete_delivery_company(DeleteView):
    model = DeliveryCompany
    template_name = "delete.html"
    success_url = "/list_delivery_company"
