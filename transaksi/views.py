from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kavling.models import Kavling
from website.models import Site
from transaksi.forms import *
from django.db import transaction
from django.contrib import messages

# Create your views here.
@login_required
def transaksi_index(request):
    context = {
        'kavlings': Kavling.objects.all(),
        'kavling': Site.objects.get(pk=1),
        'title': 'Transaksi'
    }
    return render(request, 'backstore/transaksi/index.html', context)

def transaksi_form(request, unique_id):
    context = {
        'kavling': Kavling.objects.get(unique_id=unique_id),
        'form': TransaksiForm(),
        'form_cash': TransaksiFormCash(),
        'form_kredit': TransaksiFormKredit(),
        'form_booking': TransaksiFormBooking(),
        'title': 'Buat Transaksi'
    }
    return render(request, 'backstore/transaksi/create.html', context)

def transaksi_create(request):
    redirect_url = 'penjualan'
    if request.POST:
        try:
            with transaction.atomic():
                form = TransaksiForm(request.POST)
                if form.is_valid():
                    transaksi = form.save(commit=False)
                    transaksi.kavling_id = request.POST['kavling_id']
                    transaksi.customer_id = request.POST['customer']
                    transaksi.marketing_id = request.POST['marketing']
                    if request.POST.get('tipe_transaksi') == "0":
                        transaksi.pembelian_booking = request.POST['pembelian_booking']
                        transaksi.tanggal_batas_booking = request.POST['tanggal_batas_booking']
                        transaksi.keterangan = request.POST['keterangan']
                        
                        kavling = Kavling.objects.get(pk=request.POST['kavling_id'])
                        kavling.status = 1
                        kavling.save()
                    elif request.POST.get('tipe_transaksi') == "1":
                        transaksi.pembayaran_cash = request.POST['pembayaran_cash']
                        transaksi.is_lunas = 1
                        transaksi.keterangan = request.POST['keterangan']
                        
                        kavling = Kavling.objects.get(pk=request.POST['kavling_id'])
                        kavling.status = 2
                        kavling.save()
                    elif request.POST.get('tipe_transaksi') == "2":
                        transaksi.dp = request.POST['dp']
                        transaksi.tenor = request.POST['tenor']
                        transaksi.cicilan_per_bulan = request.POST['cicilan_per_bulan']
                        transaksi.tanggal_tempo = request.POST['tanggal_tempo']
                        transaksi.keterangan = request.POST['keterangan']
                        
                        kavling = Kavling.objects.get(pk=request.POST['kavling_id'])
                        kavling.status = 2
                        kavling.save()
                        
                    transaksi.save()
                    messages.success(request, "Berhasil membuat transaksi")
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal membuat transasksi {e}")
            return redirect(redirect_url)
        
@login_required
def penjualan_index(request):
    context = {
        'datas': Transaksi.objects.all(),
        'title': 'Penjualan'
    }
    return render(request, 'backstore/penjualan/index.html', context)