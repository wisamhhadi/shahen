from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from captain.models import Captain
from core.models import Admin, PermissionGroup, Language, Country, Province, Specialty, CarCompany, CarModel, CarColor, \
    CarCategory, GoodsType, Trailer, CarLetter, CarSize, ActivityType, Car, Pay, PrePaid, Notification, Info, Banner, \
    Blog
from deliverycompany.models import DeliveryCompany
from mandob.models import Mandob, Attendance, Report, Question, Answer, OrderReport, CustomReport
from order.models import Order, OrderCar
from user.models import User
from django.forms.widgets import TimeInput, DateInput, TextInput, Select, CheckboxInput
from core.models import Fine


class GenericForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})


class admin_form(UserCreationForm):
    class Meta:
        model = Admin
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'password', 'is_superuser',
                   'device_id', 'company', 'employee', 'deleted_at', 'restored_at', 'transaction_id']

    def save(self, commit=True):
        super(admin_form, self).save()
        self.instance.set_password(self.cleaned_data['password1'])
        self._save_m2m()
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})


class admin_form_update(GenericForm):
    class Meta:
        model = Admin
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_superuser',
                   'device_id', 'company', 'employee']

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:

            if 'password' in self.changed_data:
                self.instance.set_password(self.instance.password)
            self.instance.save()
            self.instance.set_password(self.instance.password)
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class captain_form(UserCreationForm):
    class Meta:
        model = Captain
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'password', 'is_superuser',
                   'device_id', 'employee']

        widgets = {
            'car_id_expire': DateInput(attrs={'class': 'form-control','type': 'date'}),
        }

    def save(self, commit=True):
        super(captain_form, self).save()
        self.instance.set_password(self.cleaned_data['password1'])
        self._save_m2m()
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})


class captain_form_update(GenericForm):
    class Meta:
        model = Captain
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'is_superuser',
                   'device_id', 'employee']

        widgets = {
            'car_id_expire': DateInput(attrs={'class': 'form-control','type': 'date'}),

        }

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:

            if 'password' in self.changed_data:
                self.instance.set_password(self.instance.password)
            self.instance.save()
            self.instance.set_password(self.instance.password)
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class delivery_company_form(UserCreationForm):
    class Meta:
        model = DeliveryCompany
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'password', 'is_superuser',
                   'device_id', 'company', 'employee']

    def save(self, commit=True):
        super(delivery_company_form, self).save()
        self.instance.set_password(self.cleaned_data['password1'])
        self._save_m2m()
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})


class delivery_company_form_update(GenericForm):
    class Meta:
        model = DeliveryCompany
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'is_superuser',
                   'device_id', 'company', 'employee']

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:

            if 'password' in self.changed_data:
                self.instance.set_password(self.instance.password)
            self.instance.save()
            self.instance.set_password(self.instance.password)
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class mandob_form(UserCreationForm):
    class Meta:
        model = Mandob
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'password', 'is_superuser',
                   'device_id', 'company', 'employee']
        widgets = {
            'shift_start': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'shift_stop': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }



    def save(self, commit=True):
        super(mandob_form, self).save()
        self.instance.set_password(self.cleaned_data['password1'])
        self._save_m2m()
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})


class mandob_form_update(GenericForm):
    class Meta:
        model = Mandob
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'is_superuser',
                   'device_id', 'company', 'employee']
        widgets = {
            'shift_start': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'shift_stop': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            # 'balance': TextInput(attrs={'readonly': 'true', 'disabled': 'true', 'class': 'form-control'}),

        }
        # readonly_fields = ['balance']

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:

            if 'password' in self.changed_data:
                self.instance.set_password(self.instance.password)
            self.instance.save()
            self.instance.set_password(self.instance.password)
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class order_form(GenericForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'password', 'is_superuser',
                   'device_id', 'employee']


class order_car_form(GenericForm):
    class Meta:
        model = OrderCar
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'is_superuser',
                   'device_id', 'company', 'employee']


class user_form(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'password', 'is_superuser',
                   'device_id', 'company', 'employee']

    def save(self, commit=True):
        super(user_form, self).save()
        self.instance.set_password(self.cleaned_data['password1'])
        self._save_m2m()
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})


class user_form_update(GenericForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['last_login', 'is_deleted', 'groups', 'user_permissions', 'is_staff', 'is_superuser',
                   'device_id', 'company', 'employee']

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:

            if 'password' in self.changed_data:
                self.instance.set_password(self.instance.password)
            self.instance.save()
            self.instance.set_password(self.instance.password)
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return self.instance


class permission_group_form(GenericForm):
    class Meta:
        model = PermissionGroup
        fields = '__all__'
        exclude = ['employee']


class language_form(GenericForm):
    class Meta:
        model = Language
        fields = ['name', 'is_active']
        exclude = ['employee']


class attendance_form(GenericForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['employee']


class report_form(GenericForm):
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['employee']


class mandob_question_form(GenericForm):
    class Meta:
        model = Question
        fields = ['title', 'answer_type', 'is_active']


class order_report_form(GenericForm):
    class Meta:
        model = OrderReport
        fields = '__all__'
        exclude = ['employee']


class country_form(GenericForm):
    class Meta:
        model = Country
        fields = '__all__'
        exclude = ['employee']


class province_form(GenericForm):
    class Meta:
        model = Province
        fields = '__all__'
        exclude = ['employee']


class specialty_form(GenericForm):
    class Meta:
        model = Specialty
        fields = '__all__'
        exclude = ['employee']


class car_company_form(GenericForm):
    class Meta:
        model = CarCompany
        fields = '__all__'
        exclude = ['employee']


class car_model_form(GenericForm):
    class Meta:
        model = CarModel
        fields = '__all__'
        exclude = ['employee']


class car_color_form(GenericForm):
    class Meta:
        model = CarColor
        fields = '__all__'
        exclude = ['employee']


class car_category_form(GenericForm):
    class Meta:
        model = CarCategory
        fields = '__all__'
        exclude = ['employee']


class goods_type_form(GenericForm):
    class Meta:
        model = GoodsType
        fields = '__all__'
        exclude = ['employee']


class trailer_form(GenericForm):
    class Meta:
        model = Trailer
        fields = '__all__'
        exclude = ['employee']


class car_letter_form(GenericForm):
    class Meta:
        model = CarLetter
        fields = '__all__'
        exclude = ['employee']


class car_size_form(GenericForm):
    class Meta:
        model = CarSize
        fields = '__all__'
        exclude = ['employee']


class activity_type_form(GenericForm):
    class Meta:
        model = ActivityType
        fields = '__all__'
        exclude = ['employee']


class car_form(GenericForm):
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['employee']


class pay_form(GenericForm):
    class Meta:
        model = Pay
        fields = '__all__'
        exclude = ['employee']


class pre_paid_form(GenericForm):
    class Meta:
        model = PrePaid
        fields = '__all__'
        exclude = ['employee']


class notification_form(GenericForm):
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['employee']


class info_form(GenericForm):
    class Meta:
        model = Info
        fields = '__all__'
        exclude = ['employee']


class banner_form(GenericForm):
    class Meta:
        model = Banner
        fields = '__all__'
        exclude = ['employee']


class blog_form(GenericForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['employee']


class report_form(GenericForm):
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['employee']


class answer_form(GenericForm):
    class Meta:
        model = Answer
        fields = '__all__'
        exclude = ['employee']


class CustomReportForm(ModelForm):
    class Meta:
        model = CustomReport
        fields = ['title', 'target_type', 'mandob', 'is_active']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control form-control-lg border-2',
                'placeholder': 'أدخل عنوان التقرير...'
            }),
            'target_type': Select(attrs={
                'class': 'form-control border-2'
            }),
            'mandob': Select(attrs={
                'class': 'form-control border-2'
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mandob'].queryset = Mandob.objects.filter(is_active=True)
        self.fields['mandob'].required = False
        self.fields['mandob'].empty_label = "جميع المندوبين"


class fine_form(GenericForm):
    class Meta:
        model = Fine
        fields = '__all__'
        exclude = ['employee']