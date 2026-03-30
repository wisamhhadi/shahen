from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import fine_filter
from ..forms import *
from home.generics import filter_view_generic

@method_decorator(login_required(), name="dispatch")
class create_fine(CreateView):
    model = Fine
    template_name = "create_fine.html"
    success_url = "/list_fine"
    form_class = fine_form

@method_decorator(login_required(), name="dispatch")
class list_fine(filter_view_generic):
    queryset = Fine.objects.all().order_by('-id')
    model = Fine
    template_name = "list_fine.html"
    paginate_by = 25
    filterset_class = fine_filter
    context_object_name = "objects"

@method_decorator(login_required(), name="dispatch")
class update_fine(UpdateView):
    model = Fine
    template_name = "update_fine.html"
    success_url = "/list_fine"
    form_class = fine_form

@method_decorator(login_required(), name="dispatch")
class delete_fine(DeleteView):
    model = Fine
    template_name = "delete.html"
    success_url = "/list_fine" 