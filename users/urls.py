from django.urls import path
from .views import *

urlpatterns = [
    path('', index_page, name='index_page'),
    path('home_page/', home_page, name='home_page'),
    path('main_order/', main_order, name='main_order'),
    path('order_page/', order_page, name='order_page'),
]