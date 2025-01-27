from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import *
from . import services


def login_required_decorator(func):
    return login_required(func, login_url='login_page')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect("login_page")


def login_page(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_dashboard')
    return render(request, 'dashboard/login.html')


@login_required_decorator
def main_dashboard(request):
    categories = services.get_data_from_table('users_category')
    products = services.get_data_from_table('users_product')
    customers = services.get_data_from_table('users_customer')
    orders = services.get_data_from_table('users_order')
    table_list = services.get_table()
    ctx = {
        'counts': {
            'categories': len(categories),
            'products': len(products),
            'customers': len(customers),
            'orders': len(orders),
        },
        'table_list': table_list
    }
    return render(request, 'dashboard/index.html', ctx)


# CATEGORY
@login_required_decorator
def category_list(request):
    categories = Category.objects.all()
    ctx = {
        'categories': categories
    }
    return render(request, 'dashboard/category/list.html', ctx)


@login_required_decorator
def category_create(request):
    """Ushbu metod mahsulot kategoriyalarini yaratadi, masalan, Pizza, Burger va boshqalar."""
    model = Category()
    form = CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('category_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_edit(request, pk):
    model = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('category_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_delete(request, pk):
    model = Category.objects.get(pk=pk)
    model.delete()
    return redirect('category_list')


# PRODUCT
@login_required_decorator
def product_list(request):
    products = Product.objects.all()
    ctx = {
        'products': products
    }
    return render(request, 'dashboard/product/list.html', ctx)


@login_required_decorator
def product_create(request):
    model = Product()
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('product_list')
    else:
        print(form.errors)
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/product/form.html', ctx)


@login_required_decorator
def product_edit(request, pk):
    model = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('product_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/product/form.html', ctx)


@login_required_decorator
def product_delete(request, pk):
    model = Product.objects.get(pk=pk)
    model.delete()
    return redirect('product_list')


##CUSTOMER##
@login_required_decorator
def user_list(request):
    users = Customer.objects.all()
    ctx = {
        'users': users
    }
    return render(request, 'dashboard/customer/list.html', ctx)


@login_required_decorator
def user_create(request):
    model = Customer()
    form = CustomerForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('user_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/customer/form.html', ctx)


@login_required_decorator
def user_edit(request, pk):
    model = Customer.objects.get(pk=pk)
    form = CustomerForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('user_list')
    ctx = {
        'model': model,
        'form': form
    }
    return render(request, 'dashboard/customer/form.html', ctx)


@login_required_decorator
def user_delete(request, pk):
    model = Customer.objects.get(pk=pk)
    model.delete()
    return redirect('user_list')


##ORDER##
@login_required_decorator
def order_list(request):
    orders = Order.objects.all()
    ctx = {
        'orders': orders
    }
    return render(request, 'dashboard/order/list.html')


@login_required_decorator
def customer_order_list(request, id):
    customer_orders = services.get_order_by_user(id=id)
    ctx = {
        'customer_orders': customer_orders
    }
    return render(request, 'dashboard/customer_order/list.html', ctx)


@login_required_decorator
def orderproduct_list(request, id):
    productorders = services.get_product_by_order(id=id)
    ctx = {
        'productorders': productorders
    }
    return render(request, 'dashboard/productorder/list.html', ctx)
