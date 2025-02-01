import json

from django.shortcuts import render, redirect
from django.http import JsonResponse

from .services import *
from .forms import *
from config.settings import MEDIA_ROOT


def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get('product_id', 0))
        return JsonResponse(product)


def index_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get('orders')
    total_price = request.COOKIES.get('total_price', 0)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                    'product': Product.objects.filter(pk=int(key)),
                    'count': val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }
    response = render(request, 'users/index.html', ctx)
    return response


def main_order(request):
    if request.POST:
        try:
            model = Customer.objects.get(phone_number=request.POST.get("phone_number", ""))
        except:
            model = Customer()
        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            formOrder = OrderForm(request.POST or None, instance=Order())
            if formOrder.is_valid():
                order = formOrder.save(customer=customer)
                print("order:", order)
                order_list = request.COOKIES.get("orders")

                for key, value in json.loads(order_list).items():
                    product = get_product_by_id(int(key))

                    counts = value
                    order_product = OrderProduct(
                        count=counts,
                        price=product['price'],
                        product_id=product['id'],
                        order_id=order.id
                    )
                    order_product.save()
                return redirect("index_page")
            else:
                print(formOrder.errors)
        else:
            print(form.errors)

    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    order_list = request.COOKIES.get('orders')
    total_price = request.COOKIES.get('total_price')
    if order_list:
        for key, val in json.loads(order_list).items():
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    'count': val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT,
    }
    response = render(request, 'users/order.html', ctx)
    return response


def order_page(request):
    if request.GET:
        user = get_user_by_phone(request.GET.get("phone_number",0))
        return JsonResponse(user)
