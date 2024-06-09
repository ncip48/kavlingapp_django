# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    
    path('panel/dashboard', dashboard, name='dashboard'),
    #user
    path('panel/user', user_index, name='user'),
    path('panel/user/create', user_create, name='user_create'),
    path('panel/user/update/<int:user_id>', user_update, name='user_update'),
    path('panel/user/delete/<int:user_id>', user_delete, name='user_delete'),
    #kavling
    path('panel/kavling', kavling_index, name='kavling'),
    path('panel/kavling/create', kavling_create, name='kavling_create'),
    path('panel/kavling/update/<int:kavling_id>', kavling_update, name='kavling_update'),
    path('panel/kavling/delete/<int:kavling_id>', kavling_delete, name='kavling_delete'),
]