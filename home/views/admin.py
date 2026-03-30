from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import admin_filter
from home.forms import *
from home.generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_admin(CreateView):
    model = Admin
    template_name = "create_admin.html"
    success_url = "/list_admin"
    form_class = admin_form


@method_decorator(login_required(), name="dispatch")
class list_admin(filter_view_generic):
    queryset = Admin.objects.all().order_by('-id')
    model = Admin
    template_name = "list_admin.html"
    paginate_by = 25
    filterset_class = admin_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_admin(UpdateView):
    model = Admin
    template_name = "update_admin.html"
    success_url = "/list_admin"
    form_class = admin_form_update


@method_decorator(login_required(), name="dispatch")
class delete_admin(DeleteView):
    model = Admin
    template_name = "delete.html"
    success_url = "/list_admin"
