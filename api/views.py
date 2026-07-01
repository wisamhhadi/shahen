from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserProfileSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    phone = request.data.get('phone')
    password = request.data.get('password')

    if not phone or not password:
        return Response(
            {'detail': 'phone and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=phone, password=password)

    if user is None:
        # بعض الأنظمة تخزن الهاتف بدون الصفر الأول
        if str(phone).startswith('0'):
            user = authenticate(request, username=str(phone)[1:], password=password)

    if user is None:
        return Response(
            {'detail': 'Invalid phone or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user': UserProfileSerializer(user).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_me(request):
    return Response({
        'user': UserProfileSerializer(request.user).data
    })