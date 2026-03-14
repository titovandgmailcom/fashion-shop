from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Size

User = get_user_model()

class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('paid', 'Оплачен'),
        ('delivery', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'Картой онлайн'),
        ('card_courier', 'Картой курьеру'),
    ]
    
    DELIVERY_CHOICES = [
        ('courier', 'Курьер'),
        ('pickup', 'Самовывоз'),
        ('post', 'Почта'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, verbose_name='Способ доставки')
    delivery_address = models.TextField(blank=True, verbose_name='Адрес доставки')
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость доставки')
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма товаров')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итого')
    
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ {self.order_number}"

class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    product_name = models.CharField(max_length=200, verbose_name='Название товара')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер')
    size_name = models.CharField(max_length=20, verbose_name='Размер')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"