from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product, Category

@api_view(['GET'])
def product_list(request):
    """Список товаров с фильтрацией"""
    products = Product.objects.filter(is_active=True)
    
    # Фильтры
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(price__lte=max_price)
    
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Сортировка
    ordering = request.GET.get('ordering', '-created_at')
    products = products.order_by(ordering)
    
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'price': float(product.price),
            'old_price': float(product.old_price) if product.old_price else None,
            'main_image': product.images.filter(is_main=True).first().image.url if product.images.exists() else None,
            'is_new': product.is_new,
            'is_bestseller': product.is_bestseller,
        })
    
    return Response(result)

@api_view(['GET'])
def product_detail(request, product_id):
    """Детальная информация о товаре"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    images = []
    for image in product.images.all():
        images.append({
            'id': image.id,
            'url': image.image.url,
            'is_main': image.is_main,
        })
    
    sizes = []
    for size in product.sizes.all():
        sizes.append({
            'id': size.size.id,
            'name': size.size.name,
            'quantity': size.quantity,
        })
    
    return Response({
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'description': product.description,
        'price': float(product.price),
        'old_price': float(product.old_price) if product.old_price else None,
        'vendor_code': product.vendor_code,
        'category_id': product.category.id,
        'category_name': product.category.name,
        'images': images,
        'sizes': sizes,
        'model_url': product.model_url,
        'size_chart': product.size_chart.url if product.size_chart else None,
        'composition': product.composition,
        'country': product.country,
        'is_new': product.is_new,
        'is_bestseller': product.is_bestseller,
    })

@api_view(['GET'])
def new_products(request):
    """Новинки"""
    products = Product.objects.filter(is_active=True, is_new=True)[:10]
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'main_image': product.images.filter(is_main=True).first().image.url if product.images.exists() else None,
        })
    return Response(result)

@api_view(['GET'])
def bestsellers(request):
    """Хиты продаж"""
    products = Product.objects.filter(is_active=True, is_bestseller=True)[:10]
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'main_image': product.images.filter(is_main=True).first().image.url if product.images.exists() else None,
        })
    return Response(result)

@api_view(['GET'])
def category_list(request):
    """Список категорий"""
    categories = Category.objects.filter(is_active=True)
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'parent_id': category.parent.id if category.parent else None,
            'image': category.image.url if category.image else None,
        })
    return Response(result)