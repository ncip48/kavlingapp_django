# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    
    #SVG Editor
    path('panel/svg', svg, name='svg'),
    #dashboard
    path('panel/dashboard', dashboard, name='dashboard'),
    #user
    path('panel/user', user_index, name='user'),
    path('panel/user/list', user_list, name='user_list'),
    path('panel/user/create', user_create, name='user_create'),
    path('panel/user/update/<int:user_id>', user_update, name='user_update'),
    path('panel/user/delete/<int:user_id>', user_delete, name='user_delete'),
    #kavling
    path('panel/kavling', kavling_index, name='kavling'),
    path('panel/kavling/create', kavling_create, name='kavling_create'),
    path('panel/kavling/import', kavling_import, name='kavling_import'),
    path('panel/kavling/template', kavling_template, name='kavling_template'),
    path('panel/kavling/update/<int:kavling_id>', kavling_update, name='kavling_update'),
    path('panel/kavling/delete/<int:kavling_id>', kavling_delete, name='kavling_delete'),
    #marketing
    path('panel/marketing', marketing_index, name='marketing'),
    path('panel/marketing/create', marketing_create, name='marketing_create'),
    path('panel/marketing/update/<int:marketing_id>', marketing_update, name='marketing_update'),
    path('panel/marketing/delete/<int:marketing_id>', marketing_delete, name='marketing_delete'),
    #customer
    path('panel/customer', customer_index, name='customer'),
    path('panel/customer/create', customer_create, name='customer_create'),
    path('panel/customer/update/<int:customer_id>', customer_update, name='customer_update'),
    path('panel/customer/delete/<int:customer_id>', customer_delete, name='customer_delete'),
]