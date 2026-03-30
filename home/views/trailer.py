from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from home.filters import trailer_filter
from ..forms import *
from home.generics import filter_view_generic


@method_decorator(login_required(), name="dispatch")
class create_trailer(CreateView):
    model = Trailer
    template_name = "create_trailer.html"
    success_url = "/list_trailer"
    form_class = trailer_form


@method_decorator(login_required(), name="dispatch")
class list_trailer(filter_view_generic):
    queryset = Trailer.objects.all().order_by('-id')
    model = Trailer
    template_name = "list_trailer.html"
    paginate_by = 25
    filterset_class = trailer_filter
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_trailer(UpdateView):
    model = Trailer
    template_name = "update_trailer.html"
    success_url = "/list_trailer"
    form_class = trailer_form


@method_decorator(login_required(), name="dispatch")
class delete_trailer(DeleteView):
    model = Trailer
    template_name = "delete.html"
    success_url = "/list_trailer"
