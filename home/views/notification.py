from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView,ListView
from ..forms import *


@method_decorator(login_required(), name="dispatch")
class create_notification(CreateView):
    model = Notification
    template_name = "create_notification.html"
    success_url = "/list_notification"
    form_class = notification_form


@method_decorator(login_required(), name="dispatch")
class list_notification(ListView):
    queryset = Notification.objects.all().order_by('-id')
    model = Notification
    template_name = "list_notification.html"
    paginate_by = 25
    context_object_name = "objects"


@method_decorator(login_required(), name="dispatch")
class update_notification(UpdateView):
    model = Notification
    template_name = "update_notification.html"
    success_url = "/list_notification"
    form_class = notification_form


@method_decorator(login_required(), name="dispatch")
class delete_notification(DeleteView):
    model = Notification
    template_name = "delete.html"
    success_url = "/list_notification"
