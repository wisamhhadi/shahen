from excel_response import ExcelView

from captain.models import Captain
from core.models import *
from deliverycompany.models import DeliveryCompany
from mandob.models import Mandob, Attendance
from order.models import Order, OrderCar
from user.models import User


class admin_excel(ExcelView):
    model = Admin


class language_excel(ExcelView):
    model = Language


class mandob_excel(ExcelView):
    model = Mandob


class attendance_excel(ExcelView):
    model = Attendance


class country_excel(ExcelView):
    model = Country


class province_excel(ExcelView):
    model = Province


class specialty_excel(ExcelView):
    model = Specialty


class car_company_excel(ExcelView):
    model = CarCompany


class car_model_excel(ExcelView):
    model = CarModel


class car_color_excel(ExcelView):
    model = CarColor


class car_category_excel(ExcelView):
    model = CarCategory


class goods_type_excel(ExcelView):
    model = GoodsType


class trailer_excel(ExcelView):
    model = Trailer


class car_letter_excel(ExcelView):
    model = CarLetter


class car_size_excel(ExcelView):
    model = CarSize


class activity_type_excel(ExcelView):
    model = ActivityType


class delivery_company_excel(ExcelView):
    model = DeliveryCompany


class car_excel(ExcelView):
    model = Car


class captain_excel(ExcelView):
    model = Captain


class user_excel(ExcelView):
    model = User


class order_excel(ExcelView):
    model = Order


class order_car_excel(ExcelView):
    model = OrderCar


class pay_excel(ExcelView):
    model = Pay


class pre_paid_excel(ExcelView):
    model = PrePaid
