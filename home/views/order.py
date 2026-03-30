from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import order_filter
from ..forms import *
from home.generics import filter_view_generic
from order.models import Order, OrderCar


@method_decorator(login_required(), name="dispatch")
class create_order(CreateView):
    model = Order
    template_name = "create_order.html"
    success_url = "/list_order"
    form_class = order_form


@method_decorator(login_required(), name="dispatch")
class list_order(filter_view_generic):
    queryset = Order.objects.all().order_by('-id')
    model = Order
    template_name = "list_order.html"
    paginate_by = 25
    filterset_class = order_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_order(UpdateView):
    model = Order
    template_name = "update_order.html"
    success_url = "/list_order"
    form_class = order_form


@method_decorator(login_required(), name="dispatch")
class delete_order(DeleteView):
    model = Order
    template_name = "delete.html"
    success_url = "/list_order"




@method_decorator(login_required(), name="dispatch")
class update_order_car(UpdateView):
    model = OrderCar
    template_name = "update_order.html"
    success_url = "/list_order"
    form_class = order_car_form


@method_decorator(login_required(), name="dispatch")
class delete_order_car(DeleteView):
    model = OrderCar
    template_name = "delete.html"
    success_url = "/list_order_car"
