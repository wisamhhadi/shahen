from rest_framework import serializers
from django.contrib.auth import get_user_model

from mandob.models import Mandob, OrderReport, OrderReportItem
from captain.models import Captain
from deliverycompany.models import DeliveryCompany
from order.models import Order, OrderCar, OrderOffer
from user.models import User as ClientUser


AuthUser = get_user_model()


class FileURLMixin:
    def build_file_url(self, obj, field_name):
        file_field = getattr(obj, field_name, None)
        if not file_field:
            return None

        try:
            url = file_field.url
        except Exception:
            return None

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(url)
        return url


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = [
            "id",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class MandobSerializer(FileURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    province_name = serializers.CharField(source="province.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Mandob
        fields = [
            "id",
            "name",
            "phone",
            "status",
            "is_active",
            "is_logged",
            "is_free",
            "balance",
            "city",
            "location",
            "latitude",
            "longitude",
            "latitude_base",
            "longitude_base",
            "radius",
            "province_name",
            "country_name",
            "image_url",
            "created",
            "updated",
        ]

    def get_image_url(self, obj):
        return self.build_file_url(obj, "image")


class CaptainSerializer(FileURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    province_name = serializers.CharField(source="province.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Captain
        fields = [
            "id",
            "name",
            "phone",
            "status",
            "is_active",
            "is_logged",
            "city",
            "location",
            "latitude",
            "longitude",
            "latitude_base",
            "longitude_base",
            "province_name",
            "country_name",
            "company_name",
            "image_url",
            "created",
            "updated",
        ]

    def get_image_url(self, obj):
        return self.build_file_url(obj, "image")


class DeliveryCompanySerializer(FileURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    province_name = serializers.CharField(source="province.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)
    specialty_name = serializers.CharField(source="specialty.name", read_only=True)

    class Meta:
        model = DeliveryCompany
        fields = [
            "id",
            "name",
            "phone",
            "is_active",
            "is_logged",
            "balance",
            "city",
            "location",
            "latitude",
            "longitude",
            "latitude_base",
            "longitude_base",
            "province_name",
            "country_name",
            "specialty_name",
            "image_url",
            "created",
            "updated",
        ]

    def get_image_url(self, obj):
        return self.build_file_url(obj, "image")


class ClientUserSerializer(FileURLMixin, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    province_name = serializers.CharField(source="province.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = ClientUser
        fields = [
            "id",
            "name",
            "phone",
            "type",
            "company_name",
            "is_active",
            "is_logged",
            "max_debt",
            "city",
            "location",
            "latitude",
            "longitude",
            "latitude_base",
            "longitude_base",
            "province_name",
            "country_name",
            "image_url",
            "created",
            "updated",
        ]

    def get_image_url(self, obj):
        return self.build_file_url(obj, "image")


class OrderCarSerializer(serializers.ModelSerializer):
    captain_name = serializers.CharField(source="captain.name", read_only=True)
    from_province_name = serializers.CharField(source="from_province.name", read_only=True)
    to_province_name = serializers.CharField(source="to_province.name", read_only=True)

    class Meta:
        model = OrderCar
        fields = [
            "id",
            "captain",
            "captain_name",
            "car",
            "trailer",
            "trailer_count",
            "goods_cost",
            "goods_count",
            "goods_details",
            "note",
            "delivery_date",
            "delivery_time",
            "from_name",
            "from_lat",
            "from_long",
            "from_province_name",
            "to_name",
            "to_lat",
            "to_long",
            "to_province_name",
            "distance",
            "is_active",
            "created",
            "updated",
        ]


class OrderOfferSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    captain_name = serializers.CharField(source="captain.name", read_only=True)

    class Meta:
        model = OrderOffer
        fields = [
            "id",
            "company",
            "company_name",
            "captain",
            "captain_name",
            "time",
            "price",
            "is_active",
            "created",
            "updated",
        ]


class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    captain_name = serializers.CharField(source="captain.name", read_only=True)
    cars = OrderCarSerializer(source="ordercar_set", many=True, read_only=True)
    offers = OrderOfferSerializer(source="orderoffer_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "user_name",
            "company",
            "company_name",
            "captain",
            "captain_name",
            "collection_area",
            "collection_area_details",
            "rejection_reason",
            "loading_workers_count",
            "loading_workers_cost",
            "delivering_workers_count",
            "delivering_workers_cost",
            "distance",
            "order_type",
            "captain_status",
            "client_status",
            "note",
            "client_rating",
            "captain_rating",
            "is_active",
            "created",
            "updated",
            "cars",
            "offers",
        ]


class OrderReportItemSerializer(FileURLMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderReportItem
        fields = [
            "id",
            "name",
            "category",
            "type",
            "count",
            "price",
            "total_price",
            "is_active",
            "created",
            "updated",
        ]


class OrderReportSerializer(serializers.ModelSerializer):
    mandob_name = serializers.CharField(source="mandob.name", read_only=True)
    items = OrderReportItemSerializer(source="orderreportitem_set", many=True, read_only=True)

    class Meta:
        model = OrderReport
        fields = [
            "id",
            "mandob",
            "mandob_name",
            "name",
            "location",
            "currency",
            "type",
            "paid",
            "last",
            "total_price",
            "note",
            "latitude",
            "longitude",
            "is_active",
            "created",
            "updated",
            "items",
        ]