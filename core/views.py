import random
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.conf import settings
from django.db.models.base import ModelBase
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from captain.models import Captain, CaptainToken
from captain.serializers import CaptainSerializer, CaptainTokenSerializer
from deliverycompany.models import DeliveryCompany, DeliveryCompanyToken
from deliverycompany.serializers import DeliveryCompanySerializer, DeliveryCompanyTokenSerializer
from mandob.models import Mandob, MandobToken
from mandob.serializers import MandobSerializer, MandobTokenSerializer
from user.models import User, UserToken
from user.serializers import UserSerializer, UserTokenSerializer

permissionsDict = {
    # 'Admin':{
    #     'GET': [IsAdminUser, IsAuthenticated],
    #     'Post': [IsAuthenticated, IsAdminUser],
    # }
}


def send_sms(to_number, message_body):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )

        return True
    except TwilioRestException as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False


class UserLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            phone = str(request.data.get('phone'))
            print(phone)

            if not User.objects.filter(phone=phone).exists():
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            user = User.objects.get(phone=phone)
            print(user.pin)

            # Case 1: Only phone provided - generate and send PIN
            if 'password' not in request.data and 'pin' not in request.data:
                pin = str(random.randint(100000, 999999))  # 6-digit PIN
                user.pin = pin
                user.save()

                twilio_phone = f"+964{phone}" if not phone.startswith('+') else phone
                message = f"Your verification code for ShahenCo is: {pin}."

                if not send_sms(twilio_phone, message):
                    return Response(
                        {'error': 'Failed to send SMS'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE
                    )

                return Response(
                    {'message': 'SMS with verification PIN sent'},
                    status=status.HTTP_200_OK
                )

            # Case 2: Password authentication
            elif 'password' in request.data:
                password = request.data.get('password')
                if not user.check_password(password):
                    return Response(
                        {'error': 'Invalid password'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

            # Case 3: PIN authentication
            elif 'pin' in request.data:
                provided_pin = str(request.data.get('pin'))
                print(provided_pin)
                if provided_pin != str(user.pin):
                    return Response(
                        {'error': 'Invalid PIN'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Clear PIN after successful verification
                user.pin = None
                user.save()

            # Generate token for successful authentications (cases 2 & 3)
            token, created = UserToken.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': UserTokenSerializer(token).data
            })

        except Exception as e:
            return Response(
                {'error': 'Authentication failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class MandobLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request,*args, **kwargs):
        try:
            phone = str(request.data.get('phone'))

            if not Mandob.objects.filter(phone=phone).exists():
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            mandob = Mandob.objects.get(phone=phone)

            # Case 1: Only phone provided - generate and send PIN
            if 'password' not in request.data and 'pin' not in request.data:
                pin = str(random.randint(100000, 999999))  # 6-digit PIN
                mandob.pin = pin
                mandob.save()

                twilio_phone = f"+964{phone}" if not phone.startswith('+') else phone
                message = f"Your verification code for ShahenCo is: {pin}."

                if not send_sms(twilio_phone, message):
                    return Response(
                        {'error': 'Failed to send SMS'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE
                    )

                return Response(
                    {'message': 'SMS with verification PIN sent'},
                    status=status.HTTP_200_OK
                )

            # Case 2: Password authentication
            elif 'password' in request.data:
                password = request.data.get('password')
                if not mandob.check_password(password):
                    return Response(
                        {'error': 'Invalid password'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

            # Case 3: PIN authentication
            elif 'pin' in request.data:
                provided_pin = str(request.data.get('pin'))
                print(provided_pin)
                if provided_pin != str(mandob.pin):
                    return Response(
                        {'error': 'Invalid PIN'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Clear PIN after successful verification
                mandob.pin = None
                mandob.save()

            # Generate token for successful authentications (cases 2 & 3)
            token, created = MandobToken.objects.get_or_create(user=mandob)
            return Response({
                'user': MandobSerializer(mandob).data,
                'token': MandobTokenSerializer(token).data
            })

        except Exception as e:
            return Response(
                {'error': 'Authentication failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class DeliveryCompanyLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request,*args, **kwargs):
        try:
            phone = str(request.data.get('phone'))

            if not DeliveryCompany.objects.filter(phone=phone).exists():
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            deliveryCompany = DeliveryCompany.objects.get(phone=phone)

            # Case 1: Only phone provided - generate and send PIN
            if 'password' not in request.data and 'pin' not in request.data:
                pin = str(random.randint(100000, 999999))  # 6-digit PIN
                deliveryCompany.pin = pin
                deliveryCompany.save()

                twilio_phone = f"+964{phone}" if not phone.startswith('+') else phone
                message = f"Your verification code for ShahenCo is: {pin}."

                if not send_sms(twilio_phone, message):
                    return Response(
                        {'error': 'Failed to send SMS'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE
                    )

                return Response(
                    {'message': 'SMS with verification PIN sent'},
                    status=status.HTTP_200_OK
                )

            # Case 2: Password authentication
            elif 'password' in request.data:
                password = request.data.get('password')
                if not deliveryCompany.check_password(password):
                    return Response(
                        {'error': 'Invalid password'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

            # Case 3: PIN authentication
            elif 'pin' in request.data:
                provided_pin = str(request.data.get('pin'))
                if provided_pin != str(deliveryCompany.pin):
                    return Response(
                        {'error': 'Invalid PIN'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Clear PIN after successful verification
                deliveryCompany.pin = None
                deliveryCompany.save()

            # Generate token for successful authentications (cases 2 & 3)
            token, created = DeliveryCompanyToken.objects.get_or_create(user=deliveryCompany)
            return Response({
                'user': DeliveryCompanySerializer(deliveryCompany).data,
                'token': DeliveryCompanyTokenSerializer(token).data
            })

        except Exception as e:
            return Response(
                {'error': 'Authentication failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class CaptainLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request,*args, **kwargs):
        try:
            phone = str(request.data.get('phone'))

            if not Captain.objects.filter(phone=phone).exists():
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            captain = Captain.objects.get(phone=phone)

            # Case 1: Only phone provided - generate and send PIN
            if 'password' not in request.data and 'pin' not in request.data:
                pin = str(random.randint(100000, 999999))  # 6-digit PIN
                captain.pin = pin
                captain.save()

                twilio_phone = f"+964{phone}" if not phone.startswith('+') else phone
                message = f"Your verification code for ShahenCo is: {pin}."

                if not send_sms(twilio_phone, message):
                    return Response(
                        {'error': 'Failed to send SMS'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE
                    )

                return Response(
                    {'message': 'SMS with verification PIN sent'},
                    status=status.HTTP_200_OK
                )

            # Case 2: Password authentication
            elif 'password' in request.data:
                password = request.data.get('password')
                if not captain.check_password(password):
                    return Response(
                        {'error': 'Invalid password'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                else:
                    token, created = CaptainToken.objects.get_or_create(user=captain)
                    return Response({
                        'user': CaptainSerializer(captain).data,
                        'token': CaptainTokenSerializer(token).data
                    })

            # Case 3: PIN authentication
            elif 'pin' in request.data:
                provided_pin = str(request.data.get('pin'))
                if provided_pin != str(captain.pin):
                    return Response(
                        {'error': 'Invalid PIN'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Clear PIN after successful verification
                captain.pin = None
                captain.save()

            # Generate token for successful authentications (cases 2 & 3)
            token, created = CaptainToken.objects.get_or_create(user=captain)
            return Response({
                'user': CaptainSerializer(captain).data,
                'token': CaptainTokenSerializer(token).data
            })

        except Exception as e:
            return Response(
                {'error': 'Authentication failed'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class GenericAutoView(GenericAPIView):
    serializer_depth = None
    model = None
    object = None
    excluded_apps = []
    excluded_models = []
    authentication_classes = []
    permissions = permissionsDict
    permission_classes = []
    filterset_class = None
    # pagination_class = None

    def setup(self, request, *args, **kwargs):
        super(GenericAutoView, self).setup(request, *args, **kwargs)
        self.set_up(*args, **kwargs)

    def set_up(self, *args, **kwargs):
        self.permission_classes = []
        self.authentication_classes = []
        # checking kwargs len
        if 2 > len(kwargs) > 3:
            raise Exception("""
            error in URL , must be /<str:app>/<str:model>
            """)

        app = kwargs['app']
        try:
            if app in settings.INSTALLED_APPS and app not in self.excluded_apps:
                app = __import__(app)
            else:
                raise Exception("""
                error : the app is not listed in SETTINGS or blocked
                """)

        except Exception as e:
            raise e

        models = getattr(app, 'models')
        # checking the model
        model = kwargs['model']
        try:
            if type(getattr(models, model)) == ModelBase and model.lower() not in self.excluded_models:
                self.model = getattr(models, model)
            else:
                raise Exception("""
                            error : you are not choosing a model or the model is blocked.
                            """)
        except Exception as e:
            raise Exception("""
            error : the model is not included in models.py ,
            %s
            """ % e)

        """
            extract per model permissions and append to the default permission_classes,
            example :
                permissions = 'model': {
                                    'get': [IsAuthenticated],
                                }     
        """
        # model_permissions = self.permissions.get(self.kwargs['model'])
        # request_permissions = model_permissions.get(self.request.method.lower())
        # for per in request_permissions:
        #     if per == AllowAny:
        #         self.authentication_classes = []
        #     else:
        #         self.authentication_classes = [TokenAuthentication]
        #     self.permission_classes.append(per)

    def get_serializer_class(self):
        """
            generate Serializer for the model .
            you can customize it depending on your model ,
            example :
                if self.model == Post:
                    self.serializer_class = post_serializer
        """

        if self.serializer_class is None:
            class Serializer(ModelSerializer):
                class Meta:
                    model = self.model
                    fields = '__all__'
                    depth = 0 if self.serializer_depth is None else self.serializer_depth

            return Serializer
        else:
            return self.serializer_class

    def get_object(self):
        """
            return an instance from pk in the url
        """
        pk = self.kwargs['pk']
        obj = get_object_or_404(self.model, pk=pk)
        return obj

    def get_queryset(self):
        """
            get queryset if the user didn't implement it manually,
        """
        if self.queryset is not None:
            return self.queryset
        else:
            return self.model.objects.all().filter(is_active=True)

    def get_filters(self):
        """
            dynamic filters on the selected model same as default django filter ,
            example :
                ?title__contains= any title
        """
        filters = {}
        for k, v in self.request.GET.items():
            filters[k] = v
        try:
            if 'page' in filters:
                del filters['page']
            self.queryset = self.get_queryset().filter(**filters)
        except Exception as e:
            raise e


class ListCreateAutoView(ListModelMixin,
                         CreateModelMixin,
                         GenericAutoView):
    """
    Concrete view for listing a queryset or creating an instance.
    """

    def get(self, request, *args, **kwargs):
        self.get_filters()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        user_models = (User, Captain, DeliveryCompany, Mandob)
        if isinstance(instance, user_models):
            password = self.request.data.get('password')
            if password:
                if not password.startswith('pbkdf2_sha256$'):
                    instance.set_password(password)
                    instance.save()


class RetrieveUpdateDestroyAutoView(RetrieveModelMixin,
                                    UpdateModelMixin,
                                    DestroyModelMixin,
                                    GenericAutoView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        user_models = (User, Captain, DeliveryCompany, Mandob)
        if isinstance(instance, user_models):
            password = self.request.data.get('password')
            if password:
                if not password.startswith('pbkdf2_sha256$'):
                    instance.set_password(password)
                    instance.save()
