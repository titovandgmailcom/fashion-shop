from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
import random
import string

@api_view(['POST'])
@permission_classes([AllowAny])
def phone_auth(request):
    """Авторизация по телефону"""
    phone = request.data.get('phone')
    
    if not phone:
        return Response({'error': 'Телефон обязателен'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Генерируем код
    code = ''.join(random.choices(string.digits, k=6))
    
    # Сохраняем код для пользователя
    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={'username': phone, 'verification_code': code}
    )
    if not created:
        user.verification_code = code
        user.save()
    
    return Response({'message': 'Код отправлен', 'debug_code': code})

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя"""
    data = request.data
    
    # Проверяем наличие обязательных полей
    if not data.get('phone') or not data.get('password'):
        return Response({'error': 'Телефон и пароль обязательны'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Создаем пользователя
    user = User.objects.create_user(
        username=data.get('phone'),
        phone=data.get('phone'),
        email=data.get('email', ''),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        password=data.get('password')
    )
    
    # Создаем токены
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'phone': user.phone,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    })

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Получение и обновление профиля"""
    if request.method == 'GET':
        user = request.user
        return Response({
            'id': user.id,
            'phone': user.phone,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.avatar.url if user.avatar else None,
            'date_of_birth': user.date_of_birth,
            'favorite_brands': user.favorite_brands,
            'clothing_size': user.clothing_size,
            'shoe_size': user.shoe_size,
        })
    
    # Обновление профиля
    user = request.user
    data = request.data
    
    if data.get('first_name'):
        user.first_name = data['first_name']
    if data.get('last_name'):
        user.last_name = data['last_name']
    if data.get('email'):
        user.email = data['email']
    
    user.save()
    
    return Response({'status': 'ok'})