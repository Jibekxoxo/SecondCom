from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import *
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
import datetime

def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'second/home.html', context)

def product_detail(request, id):
    product = Product.objects.get(id=id) 
    context = {'product': product}
    return render(request, 'second/info.html', context)

def women(request):
    products = Product.objects.filter(gender=2) 
    context = {'products': products}
    return render(request, 'second/women.html', context)

def men(request):
    products = Product.objects.filter(gender=1)
    context = {'products': products}
    return render(request, 'second/men.html', context)

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'second/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'second/cart.html', context)

def checkout(request):
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
   else:
      items = []
      order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
   
   context = {'items':items, 'order':order}
   return render(request, 'second/checkout.html', context)


def updateItem(request):   #связь между js
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      total = float(data['form']['total'])
      order.transaction_id = transaction_id

      if total == order.get_cart_total:
          order.complete = True
      order.save()

      if order.shipping == True:
          ShippingAddress.objects.create(
          customer = customer,
          order = order,
          address = data['shipping']['address'],
          city = data['shipping']['city'],
          state = data['shipping']['state'],
          zipcode = data['shipping']['zipcode'],
          )
    
    else:
        print('User is not logged in')
    
    return JsonResponse('Payment submitted..', safe=False)


class LoginView(LoginView):
    template_name = 'second/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')



class RegisterPage(FormView):
    template_name = 'second/register.html'
    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)
    

# def order(request, slug):
#     course = get_object_or_404(Course, slug=slug)

#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             order.user = request.user
#             order.course = course
#             form.save()
#             return render(request, 'products/home.html')
#     else:
#         form = OrderForm()
            

#     return render(request, 'products/order.html', {"form": form, 'course': course})


    



