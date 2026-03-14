from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:product_id>/', views.product_detail, name='product-detail'),
    path('products/new/', views.new_products, name='product-new'),
    path('products/bestsellers/', views.bestsellers, name='product-bestsellers'),
    path('categories/', views.category_list, name='category-list'),
]