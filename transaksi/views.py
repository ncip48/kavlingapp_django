from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from kavling.models import Kavling
from website.models import Site
from transaksi.forms import *

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
        'title': 'Buat Transaksi'
    }
    return render(request, 'backstore/transaksi/create.html', context)

def transaksi_create(request):
    context = {
        'kavlings': Kavling.objects.all(),
        'kavling': Site.objects.get(pk=1),
        'title': 'Buat Transaksi'
    }
    return render(request, 'backstore/transaksi/create.html', context)