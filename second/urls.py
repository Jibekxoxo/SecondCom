from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('view/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_Item/', views.updateItem, name="update_Item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('details/<int:id>/', views.product_detail, name='details'),


    path('women/', views.women, name="women"),
    path('men/', views.men, name="men"),

    path('login/', views.LoginView.as_view(), name="login"),
    path('login/register/', views.RegisterPage.as_view(), name="register"),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),

]