from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Категория товаров"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    sort_order = models.IntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class Size(models.Model):
    """Размеры товаров"""
    name = models.CharField(max_length=20, unique=True, verbose_name='Размер')
    sort_order = models.IntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Товар"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Старая цена')
    vendor_code = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    
    # 3D модель для AR
    model_url = models.URLField(blank=True, verbose_name='URL 3D модели')
    model_file = models.FileField(upload_to='3d_models/', null=True, blank=True, verbose_name='3D модель')
    
    # Размерная сетка
    size_chart = models.ImageField(upload_to='size_charts/', null=True, blank=True, verbose_name='Таблица размеров')
    size_measurements = models.JSONField(default=dict, blank=True, verbose_name='Замеры по размерам')
    
    composition = models.CharField(max_length=200, blank=True, verbose_name='Состав')
    country = models.CharField(max_length=100, blank=True, verbose_name='Страна производства')
    
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')
    is_bestseller = models.BooleanField(default=False, verbose_name='Хит продаж')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.vendor_code})"

class ProductImage(models.Model):
    """Изображения товара"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное')
    sort_order = models.IntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-is_main', 'sort_order']
    
    def __str__(self):
        return f"Изображение для {self.product.name}"

class ProductSize(models.Model):
    """Связь товара с размером и остатком"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='sizes',
        verbose_name='Товар'
    )
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Остаток по размеру'
        verbose_name_plural = 'Остатки по размерам'
        unique_together = ['product', 'size']
    
    def __str__(self):
        return f"{self.product.name} - {self.size.name}: {self.quantity} шт."

class ARModelRequest(models.Model):
    """Запрос на генерацию 3D модели"""
    STATUS_CHOICES = [
        ('pending', 'В очереди'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Готово'),
        ('failed', 'Ошибка'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ar_requests',
        verbose_name='Товар'
    )
    
    source_video = models.FileField(
        upload_to='ar_sources/videos/',
        null=True, blank=True,
        verbose_name='Видео (360°)'
    )
    source_images = models.JSONField(default=list, verbose_name='Изображения')
    
    generated_model = models.FileField(
        upload_to='ar_models/',
        null=True, blank=True,
        verbose_name='Готовая 3D модель'
    )
    thumbnail = models.ImageField(
        upload_to='ar_models/thumbnails/',
        null=True, blank=True,
        verbose_name='Превью'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    progress = models.IntegerField(default=0, verbose_name='Прогресс %')
    error_message = models.TextField(blank=True, verbose_name='Ошибка')
    task_id = models.CharField(max_length=100, blank=True, verbose_name='ID задачи')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'AR запрос'
        verbose_name_plural = 'AR запросы'
    
    def __str__(self):
        return f"AR для {self.product.name}"