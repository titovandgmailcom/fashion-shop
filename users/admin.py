from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'phone', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'avatar', 'date_of_birth', 'favorite_brands', 
                      'clothing_size', 'shoe_size', 'email_notifications', 'push_notifications'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'email', 'first_name', 'last_name'),
        }),
    )