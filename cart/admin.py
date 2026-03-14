from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'item_count', 'total_price', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__phone', 'session_id']
    inlines = [CartItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Товаров'
    
    def total_price(self, obj):
        return sum(item.total_price for item in obj.items.all())
    total_price.short_description = 'Сумма'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'size', 'quantity', 'total_price']
    list_filter = ['cart']
    search_fields = ['product__name']