from dal import autocomplete
from captain.models import Captain
from core.models import *
from deliverycompany.models import DeliveryCompany
from mandob.models import Mandob
from user.models import User


class permission_group_autocomplete(autocomplete.Select2QuerySetView):
    queryset = PermissionGroup.objects.all()
    model = PermissionGroup
    search_fields = ('name',)


class admin_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Admin.objects.all()
    model = Admin
    search_fields = ('name',)


class mandob_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Mandob.objects.all()
    model = Mandob
    search_fields = ('name',)


class country_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Country.objects.all()
    model = Country
    search_fields = ('name',)


class province_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Province.objects.all()
    model = Province
    search_fields = ('name',)


class delivery_company_autocomplete(autocomplete.Select2QuerySetView):
    queryset = DeliveryCompany.objects.all()
    model = DeliveryCompany
    search_fields = ('name',)


class trailer_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Trailer.objects.all()
    model = Trailer
    search_fields = ('name',)


class car_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Car.objects.all()
    model = Car
    search_fields = ('car_number',)


class captain_autocomplete(autocomplete.Select2QuerySetView):
    queryset = Captain.objects.all()
    model = Captain
    search_fields = ('name',)


class user_autocomplete(autocomplete.Select2QuerySetView):
    queryset = User.objects.all()
    model = User
    search_fields = ('name',)
