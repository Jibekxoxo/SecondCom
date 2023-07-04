from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_Item/', views.updateItem, name="update_Item"),
    
]