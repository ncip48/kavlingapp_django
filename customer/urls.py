# from django.conf.urls import url
from django.urls import path

from customer.views import *

urlpatterns = [
    #customer
    path('panel/customer', customer_index, name='customer'),
    path('panel/customer/create', customer_create, name='customer_create'),
    path('panel/customer/update/<int:customer_id>', customer_update, name='customer_update'),
    path('panel/customer/delete/<int:customer_id>', customer_delete, name='customer_delete'),   
]