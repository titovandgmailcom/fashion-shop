from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.get_cart, name='cart-detail'),
    path('cart/add/', views.add_to_cart, name='cart-add'),
    path('cart/item/<int:item_id>/', views.update_cart_item, name='cart-item-update'),
    path('cart/item/<int:item_id>/remove/', views.remove_from_cart, name='cart-item-remove'),
    path('cart/clear/', views.clear_cart, name='cart-clear'),
]