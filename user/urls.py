# from django.conf.urls import url
from django.urls import path

from user.views import *

urlpatterns = [
    #auth
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    #user
    path('panel/user', user_index, name='user'),
    path('panel/user/list', user_list, name='user_list'),
    path('panel/user/create', user_create, name='user_create'),
    path('panel/user/update/<int:user_id>', user_update, name='user_update'),
    path('panel/user/delete/<int:user_id>', user_delete, name='user_delete'),
]