from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Size

User = get_user_model()

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='cart',
        null=True, blank=True,
        verbose_name='Пользователь'
    )
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID сессии')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина {self.user or self.session_id}"

class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'product', 'size']
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity