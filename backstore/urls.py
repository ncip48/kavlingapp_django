# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    
    path('panel/dashboard', dashboard, name='dashboard'),
    path('panel/user', UserView().user_index, name='user'),
    path('panel/user/create', UserView().user_create, name='user_create'),
    path('panel/user/update/<int:user_id>', UserView().user_update, name='user_update'),
]