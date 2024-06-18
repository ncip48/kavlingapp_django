# from django.conf.urls import url
from django.urls import path

from dashboard.views import *

urlpatterns = [
    #dashboard
    path('panel/dashboard', dashboard, name='dashboard'),
]