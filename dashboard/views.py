from django.shortcuts import render
from django.db.models import Sum
from kavling.models import Kavling
from website.models import Site
from transaksi.models import Transaksi, Cicilan
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models.functions import ExtractDay
from django.db.models import Q

# Create your views here.
@login_required
# @permission_required('dashboard.index')
def dashboard(request):
    totalKredit = Transaksi.objects.filter(tipe_transaksi=2).aggregate(Sum('tenor'))['tenor__sum'] or 0
    sisaKredit = Cicilan.objects.count()
    
    given_date = int(datetime.now().strftime("%d"))
    seven_days_before = (given_date + 7) % 31  # Adjust for month boundaries if needed
    print(given_date, seven_days_before)
    tagihanTerdekat = Transaksi.objects.annotate(
    day_of_tempo=ExtractDay('tanggal_tempo')
    ).filter(
        Q(day_of_tempo__range=[10, 17]),
        tipe_transaksi=2
    )
    print(tagihanTerdekat)
    context = {
        'kavlings': Kavling.objects.all(),
        'kavling': Site.objects.get(pk=1),
        'count': {
            'tersedia': Kavling.objects.filter(status=0).count(),
            'booking': Kavling.objects.filter(status=1).count(),
            'kredit': Kavling.objects.filter(transaksi__tipe_transaksi=2).count(),
            'cash': Kavling.objects.filter(transaksi__tipe_transaksi=1).count(),
            'totalKredit': totalKredit,
            'sisaKredit': sisaKredit,
        },
        'tagihanTerdekat': tagihanTerdekat,
        'title': 'Dashboard'
    }
    return render(request, 'backstore/dashboard.html', context)
