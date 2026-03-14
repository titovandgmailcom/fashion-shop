from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:order_id>/', views.order_detail, name='order-detail'),
    path('orders/create/', views.create_order, name='order-create'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='order-cancel'),
]