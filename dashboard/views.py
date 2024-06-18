from django.shortcuts import render
from django.db.models import Sum
from kavling.models import Kavling
from website.models import Site
from transaksi.models import Transaksi
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
# @permission_required('dashboard.index')
def dashboard(request):
    totalKredit = Transaksi.objects.filter(tipe_transaksi=2).aggregate(Sum('tenor'))['tenor__sum'] or 0
    context = {
        'kavlings': Kavling.objects.all(),
        'kavling': Site.objects.get(pk=1),
        'count': {
            'tersedia': Kavling.objects.filter(status=0).count(),
            'booking': Kavling.objects.filter(status=1).count(),
            'kredit': Kavling.objects.filter(transaksi__tipe_transaksi=2).count(),
            'cash': Kavling.objects.filter(transaksi__tipe_transaksi=1).count(),
            'totalKredit': totalKredit
            # 'sisaKredit': 
        },
        'title': 'Dashboard'
    }
    return render(request, 'backstore/dashboard.html', context)
