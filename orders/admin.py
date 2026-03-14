from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'product_price', 'size', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'full_name', 'total', 'status_colored', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'delivery_method', 'payment_method']
    search_fields = ['order_number', 'user__phone', 'full_name', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = [
        ('Основное', {
            'fields': ['order_number', 'user', 'status', 'is_paid']
        }),
        ('Клиент', {
            'fields': ['full_name', 'phone', 'email']
        }),
        ('Доставка', {
            'fields': ['delivery_method', 'delivery_address', 'delivery_price']
        }),
        ('Оплата', {
            'fields': ['payment_method']
        }),
        ('Детали заказа', {
            'fields': ['subtotal', 'total', 'comment']
        }),
        ('Даты', {
            'fields': ['created_at', 'updated_at']
        }),
    ]
    
    def status_colored(self, obj):
        colors = {
            'new': 'orange',
            'processing': 'blue',
            'paid': 'green',
            'delivery': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = 'Статус'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_name', 'size_name', 'quantity', 'product_price']
    list_filter = ['order']
    search_fields = ['product_name']