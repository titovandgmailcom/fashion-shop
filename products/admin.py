from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductSize, Size, ARModelRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'sort_order']
    list_editable = ['is_active', 'sort_order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor_code', 'price', 'is_active', 'is_new', 'is_bestseller']
    list_editable = ['price', 'is_active', 'is_new', 'is_bestseller']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'vendor_code']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_order']
    list_editable = ['sort_order']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_main']
    
    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'quantity']
    list_editable = ['quantity']

@admin.register(ARModelRequest)
class ARModelRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status_colored', 'progress', 'created_at']
    list_filter = ['status']
    
    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'completed': 'green',
            'failed': 'red',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )