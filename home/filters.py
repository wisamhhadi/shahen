import django_filters
from dal.widgets import WidgetMixin
from dal_select2.widgets import Select2WidgetMixin
from django import forms
from django.urls import reverse_lazy
from django_filters.widgets import RangeWidget
from captain.models import Captain
from core.models import *
from deliverycompany.models import DeliveryCompany
from mandob.models import Mandob, Attendance, Report, OrderReport, CustomReport, History
from order.models import Order
from user.models import User


class cusQuerySetSelectMixin(WidgetMixin):
    """QuerySet support for choices."""

    def filter_choices_to_render(self, selected_choices):
        """Filter out un-selected choices if choices is a QuerySet."""
        # self.choices.queryset = self.choices.queryset.filter(
        #     pk__in=[c for c in selected_choices if c]
        # )


class cusModelSelect2(cusQuerySetSelectMixin,
                      Select2WidgetMixin,
                      forms.Select):
    """my custom widget"""


class GenericFilter(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        for field in self.filters:
            self.filters[field].field.widget.attrs.update({'class': 'form-control mg-10'})


class admin_filter(GenericFilter):
    class Meta:
        model = Admin
        fields = {
            'phone': ["exact"],
            'name': ["icontains"],
            'job_title': ["icontains"],
            'is_active': ["exact"],
        }

class mandob_filter(GenericFilter):
    class Meta:
        model = Mandob
        fields = {
            'admin': ["exact"],
            'phone': ["exact"],
            'name': ["icontains"],
            'location': ["icontains"],
            'app_language': ["exact"],
            'note': ["icontains"],
            'status': ["exact"],
            'is_active': ["exact"],
        }


class attendance_filter(GenericFilter):
    day = django_filters.DateFilter(field_name='day', lookup_expr='exact',widget=forms.DateInput(attrs={'type': 'date','class': 'form-control','placeholder': 'اختر التاريخ'}))
    class Meta:
        model = Attendance
        fields = {
            'mandob': ["exact"],
            'day': ["exact"],
            'work_hour': ["lte", "gte"],
            'is_active': ["exact"],
        }

            


class history_filter(GenericFilter):
    mandob = django_filters.CharFilter(field_name='mandob', lookup_expr='exact',
                                       widget=cusModelSelect2(url=reverse_lazy('mandob_autocomplete')))

    class Meta:
        model = History
        fields = {
            'mandob': ["exact"],
            'created': ["lte",'gte'],
            'barcode': ["exact"],
            'is_active': ["exact"],
        }


class report_filter(GenericFilter):
    mandob = django_filters.CharFilter(field_name='mandob', lookup_expr='exact',
                                       widget=cusModelSelect2(url=reverse_lazy('mandob_autocomplete')))
    class Meta:
        model = Report
        fields = {
            'mandob': ["exact"],
            'type': ["exact"],
            'created': ["lte","gte"],
            'is_active': ["exact"],
        }

class order_report_filter(GenericFilter):
    mandob = django_filters.CharFilter(field_name='mandob', lookup_expr='exact',
                                       widget=cusModelSelect2(url=reverse_lazy('mandob_autocomplete')))
    class Meta:
        model = OrderReport
        fields = {
            'mandob': ["exact"],
            'name': ["icontains"],
            'location': ["icontains"],
            'total_price': ["icontains"],
            'created': ["lte","gte"],
            'is_active': ["exact"],
        }

class province_filter(GenericFilter):
    class Meta:
        model = Province
        fields = {
            'country': ["exact"],
        }


class trailer_filter(GenericFilter):
    class Meta:
        model = Trailer
        fields = {
            'car_category': ["exact"],
            'goods_type': ["exact"],
            'name': ["icontains"],
            'is_active': ["exact"],
        }


class delivery_company_filter(GenericFilter):
    class Meta:
        model = DeliveryCompany
        fields = {
            'name': ["icontains"],
            'phone': ["exact"],
            'country': ["exact"],
            'province': ["exact"],
            'city': ["icontains"],
            'location': ["icontains"],
            'specialty': ["exact"],
            'barcode': ["exact"],
            'is_active': ["exact"],
        }


class car_filter(GenericFilter):
    class Meta:
        model = Car
        fields = {
            'captain': ["exact"],
            'company': ["exact"],
            'country': ["exact"],
            'car_letter': ["exact"],
            'car_category': ["exact"],
            'trailer': ["exact"],
            'car_company': ["exact"],
            'car_model': ["exact"],
            'car_color': ["exact"],
            'car_manu_year': ["exact"],
            'barcode': ["exact"],
            'car_number': ["icontains"],
            'is_active': ["exact"],
        }


class captain_filter(GenericFilter):
    class Meta:
        model = Captain
        fields = {
            'company': ["exact"],
            'phone': ["exact"],
            'name': ["icontains"],
            'id_number': ["exact"],
            'country': ["exact"],
            'province': ["exact"],
            'city': ["icontains"],
            'location': ["icontains"],
            'app_language': ["exact"],
            'note': ["icontains"],
            'barcode': ["exact"],
            'is_active': ["exact"],
            'status': ["exact"],
        }

class user_filter(GenericFilter):
    class Meta:
        model = User
        fields = {
            'phone': ["exact"],
            'name': ["icontains"],
            'language': ["exact"],
            'country': ["exact"],
            'province': ["exact"],
            'city': ["icontains"],
            'location': ["icontains"],
            'type': ["exact"],
            'barcode': ["exact"],
            'is_active': ["exact"],
        }


class pay_filter(GenericFilter):
    class Meta:
        model = Pay
        fields = {
            'user': ["exact"],
            'company': ["exact"],
            'captain': ["exact"],
            'mandob': ["exact"],
            'user_type': ["exact"],
            'pay_type': ["exact"],
            'note': ["icontains"],
            'is_active': ["exact"],
        }


class pre_paid_filter(GenericFilter):
    class Meta:
        model = PrePaid
        fields = {
            'user': ["exact"],
            'company': ["exact"],
            'captain': ["exact"],
            'mandob': ["exact"],
            'user_type': ["exact"],
            'code': ["icontains"],
            'is_active': ["exact"],
        }


class order_filter(GenericFilter):
    class Meta:
        model = Order
        fields = {
            'user': ["exact"],
            'company': ["exact"],
            'captain': ["exact"],
            'order_type': ["exact"],
            'captain_status': ["exact"],
            'client_status': ["exact"],
            'rejection_reason': ["icontains"],
            'collection_area': ["icontains"],
            'is_active': ["exact"],
        }


class custom_report_filter(GenericFilter):
    mandob = django_filters.CharFilter(field_name='mandob', lookup_expr='exact',
                                       widget=cusModelSelect2(url=reverse_lazy('mandob_autocomplete')))
    class Meta:
        model = CustomReport
        fields = {
            'mandob': ["exact"],
            'target_type': ["exact"],
            'created': ["lte","gte"],
            'is_active': ["exact"],
        }


class fine_filter(GenericFilter):
    class Meta:
        model = Fine
        fields = {
            'user': ["exact"],
            'company': ["exact"],
            'captain': ["exact"],
            'mandob': ["exact"],
            'user_type': ["exact"],
            'note': ["icontains"],
            'is_active': ["exact"],
        }