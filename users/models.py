from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Расширенная модель пользователя"""
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    code_created_at = models.DateTimeField(null=True, blank=True)
    
    favorite_brands = models.TextField(blank=True, verbose_name='Любимые бренды')
    clothing_size = models.CharField(max_length=10, blank=True, verbose_name='Размер одежды')
    shoe_size = models.CharField(max_length=10, blank=True, verbose_name='Размер обуви')
    
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.phone})"