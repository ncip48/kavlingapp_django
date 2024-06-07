# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('signin', login_view, name="login")
]