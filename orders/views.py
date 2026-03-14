from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cart.models import Cart
from .models import Order, OrderItem

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'total': float(order.total),
            'created_at': order.created_at,
            'items_count': order.items.count(),
        })
    
    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    """Детальная информация о заказе"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    items = []
    for item in order.items.all():
        items.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product_name,
            'product_image': item.product.images.filter(is_main=True).first().image.url if item.product.images.exists() else None,
            'price': float(item.product_price),
            'size': item.size_name,
            'quantity': item.quantity,
        })
    
    return Response({
        'id': order.id,
        'order_number': order.order_number,
        'status': order.status,
        'status_display': order.get_status_display(),
        'full_name': order.full_name,
        'phone': order.phone,
        'email': order.email,
        'delivery_method': order.delivery_method,
        'delivery_address': order.delivery_address,
        'delivery_price': float(order.delivery_price),
        'payment_method': order.payment_method,
        'is_paid': order.is_paid,
        'subtotal': float(order.subtotal),
        'total': float(order.total),
        'comment': order.comment,
        'created_at': order.created_at,
        'items': items,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Создание заказа из корзины"""
    data = request.data
    
    # Проверяем обязательные поля
    required_fields = ['full_name', 'phone', 'email', 'delivery_method', 'payment_method']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'Поле {field} обязательно'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Получаем корзину пользователя
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not cart.items.exists():
        return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Рассчитываем сумму
    subtotal = sum(item.total_price for item in cart.items.all())
    delivery_price = float(data.get('delivery_price', 0))
    total = subtotal + delivery_price
    
    # Создаем заказ
    order = Order.objects.create(
        user=request.user,
        full_name=data['full_name'],
        phone=data['phone'],
        email=data['email'],
        delivery_method=data['delivery_method'],
        delivery_address=data.get('delivery_address', ''),
        delivery_price=delivery_price,
        payment_method=data['payment_method'],
        subtotal=subtotal,
        total=total,
        comment=data.get('comment', '')
    )
    
    # Переносим товары из корзины в заказ
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            product_name=cart_item.product.name,
            product_price=cart_item.product.price,
            size=cart_item.size,
            size_name=cart_item.size.name,
            quantity=cart_item.quantity
        )
        
        # Уменьшаем количество на складе
        product_size = cart_item.product.sizes.get(size=cart_item.size)
        product_size.quantity -= cart_item.quantity
        product_size.save()
    
    # Очищаем корзину
    cart.items.all().delete()
    
    return Response({
        'status': 'ok',
        'order_id': order.id,
        'order_number': order.order_number
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    """Отмена заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status not in ['new', 'processing']:
        return Response({'error': 'Заказ нельзя отменить'}, status=status.HTTP_400_BAD_REQUEST)
    
    order.status = 'cancelled'
    order.save()
    
    # Возвращаем товары на склад
    for item in order.items.all():
        product_size = item.product.sizes.get(size=item.size)
        product_size.quantity += item.quantity
        product_size.save()
    
    return Response({'status': 'ok'})