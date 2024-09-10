# from django.conf.urls import url
from django.urls import path

from transaksi.views import *

urlpatterns = [
    #transaksi
    path('panel/transaksi', transaksi_index, name='transaksi'),
    path('panel/transaksi/<uuid:unique_id>', transaksi_form, name='transaksi_form'),
    path('panel/transaksi/<int:transaksi_id>', transaksi_update, name='transaksi_update'),
    path('panel/create_transaksi', transaksi_create, name='transaksi_create'),
    path('panel/kwitansi/<uuid:unique_id>', generate_kwitansi, name='generate_kwitansi'),
    
    
    #penjualan
    path('panel/penjualan', penjualan_index, name='penjualan'),
    path('panel/penjualan/<uuid:unique_id>', penjualan_detail, name='penjualan_detail'),
    path('panel/penjualan/delete/<int:transaksi_id>', penjualan_delete, name='penjualan_delete'),
    path('panel/penjualan/invoice', generate_pdf, name='invoice'),
    
    #cicilan
    path('panel/cicilan/<int:transaksi_id>', cicilan_create, name='cicilan_create'),
    path('panel/cicilan/kwitansi/<uuid:unique_id>', generate_kwitansi_cicilan, name='generate_kwitansi_cicilan'),
    path('panel/cicilan/pdf/<uuid:unique_id>', cicilan_pdf, name='cicilan_pdf'),
    
    
]