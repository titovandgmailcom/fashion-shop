from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from products.models import Product, ProductSize
from .models import Cart, CartItem

def get_or_create_cart(request):
    """Получить или создать корзину для пользователя/сессии"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

@api_view(['GET'])
def get_cart(request):
    """Получить содержимое корзины"""
    cart = get_or_create_cart(request)
    
    items = []
    total = 0
    
    for item in cart.items.all():
        items.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_image': item.product.images.filter(is_main=True).first().image.url if item.product.images.exists() else None,
            'price': float(item.product.price),
            'size': item.size.name,
            'quantity': item.quantity,
            'total': float(item.total_price),
        })
        total += item.total_price
    
    return Response({
        'id': cart.id,
        'items': items,
        'total': float(total),
        'items_count': cart.items.count()
    })

@api_view(['POST'])
def add_to_cart(request):
    """Добавить товар в корзину"""
    product_id = request.data.get('product_id')
    size_id = request.data.get('size_id')
    quantity = request.data.get('quantity', 1)
    
    if not all([product_id, size_id]):
        return Response({'error': 'Не указан товар или размер'}, status=status.HTTP_400_BAD_REQUEST)
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    product_size = get_object_or_404(ProductSize, product_id=product_id, size_id=size_id)
    
    if product_size.quantity < quantity:
        return Response({'error': 'Недостаточно товара'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size_id=size_id,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return Response({'status': 'ok'})

@api_view(['DELETE'])
def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return Response({'status': 'ok'})

@api_view(['PUT'])
def update_cart_item(request, item_id):
    """Обновить количество товара"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'Не указано количество'}, status=status.HTTP_400_BAD_REQUEST)
    
    if quantity == 0:
        cart_item.delete()
    else:
        product_size = get_object_or_404(ProductSize, product=cart_item.product, size=cart_item.size)
        if quantity > product_size.quantity:
            return Response({'error': 'Недостаточно товара'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity = quantity
        cart_item.save()
    
    return Response({'status': 'ok'})

@api_view(['POST'])
def clear_cart(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    return Response({'status': 'ok'})