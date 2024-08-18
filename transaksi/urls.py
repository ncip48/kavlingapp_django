# from django.conf.urls import url
from django.urls import path

from transaksi.views import *

urlpatterns = [
    #transaksi
    path('panel/transaksi', transaksi_index, name='transaksi'),
    path('panel/transaksi/<uuid:unique_id>', transaksi_form, name='transaksi_form'),
    path('panel/create_transaksi', transaksi_create, name='transaksi_create'),
]