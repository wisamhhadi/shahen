from django.db.models import Q
from django_filters.views import FilterView

from mandob.models import Mandob, Attendance, Report, OrderReport


class filter_view_generic(FilterView):
    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)

        if (
                not self.filterset.is_bound
                or self.filterset.is_valid()
                or not self.get_strict()
        ):
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        # objects = self.object_list

        if self.request.GET.get('search', None) is not None:
            field_list = [f.name for f in self.model._meta.get_fields()
                          if f.concrete and not f.is_relation]

            q_objects = Q()
            for field_name in field_list:
                q_objects |= Q(**{f"{field_name}__icontains": self.request.GET.get('search')})

            self.object_list = self.object_list.filter(q_objects)

        if self.request.user.is_staff and self.request.user.is_superuser is False:
            if self.model == Mandob:
                self.object_list = self.object_list.filter(admin=self.request.user)

            if self.model in (Attendance, OrderReport,Report):
                self.object_list = self.object_list.filter(mandob__admin=self.request.user)

        context = self.get_context_data(
            filter=self.filterset, object_list=self.object_list
        )
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context