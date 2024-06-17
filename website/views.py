from django.shortcuts import render, redirect
from website.models import Site
from website.forms import SiteForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from kavling.functions.functions import handle_uploaded_file

# Create your views here.

@login_required
def site_index(request):
    site = Site.objects.get(pk=1)
    context = {
        'title': 'Pengaturan Website',
        'data': site,
        'form': SiteForm(instance=site)
    }
    return render(request, 'backstore/pengaturan_website.html', context)

@login_required
def site_update(request, site_id):
    redirect_url = 'site'
    try:
        site = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                form = SiteForm(request.POST, instance=site)
                if form.is_valid():
                    if 'logo' in request.FILES:
                        logo = handle_uploaded_file(request.FILES['logo'])
                        site.logo = logo
                    if 'ttd' in request.FILES:
                        ttd = handle_uploaded_file(request.FILES['ttd'])  
                        site.ttd = ttd
                    site.save()
                    messages.success(request, 'Berhasil mengubah data')
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal mengedit data {e}")
            return redirect(redirect_url)