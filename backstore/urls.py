# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout")
]