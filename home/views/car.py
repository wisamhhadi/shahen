from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import car_filter
from home.forms import *
from home.generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_car(CreateView):
    model = Car
    template_name = "create_car.html"
    success_url = "/list_car"
    form_class = car_form


@method_decorator(login_required(), name="dispatch")
class list_car(filter_view_generic):
    queryset = Car.objects.all().order_by('-id')
    model = Car
    template_name = "list_car.html"
    paginate_by = 25
    filterset_class = car_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_car(UpdateView):
    model = Car
    template_name = "update_car.html"
    success_url = "/list_car"
    form_class = car_form


@method_decorator(login_required(), name="dispatch")
class delete_car(DeleteView):
    model = Car
    template_name = "delete.html"
    success_url = "/list_car"
