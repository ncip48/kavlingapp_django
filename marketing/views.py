from django.shortcuts import render, redirect
from marketing.models import Marketing
from marketing.forms import MarketingForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.

@login_required
# @permission_required('catalog.awokwok', raise_exception=True)
def marketing_index(request):
    context = {
        'title': 'Marketing',
        'datas': Marketing.objects.all(),
    }
    return render(request, 'backstore/marketing/index.html', context)

@login_required
def marketing_create(request):
    redirect_url = 'marketing'
    if request.POST:
        try:
            with transaction.atomic():
                form = MarketingForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Berhasil menambahkan data")
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal menambahkan data {e}")
            return redirect(redirect_url)
    else:
        form = MarketingForm()
        context = {
            'form': form
        }
        return render(request, 'backstore/marketing/action.html', context)
    
@login_required
def marketing_update(request, marketing_id):
    redirect_url = 'marketing'
    try:
        marketing = Marketing.objects.get(pk=marketing_id)
    except Marketing.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                form = MarketingForm(request.POST, instance=marketing)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Berhasil mengubah data')
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, "Gagal mengedit data")
            return redirect(redirect_url)
    else:
        form = MarketingForm(instance=marketing)
        context = {
            'form': form, 
            'data': marketing
        }
        return render(request, 'backstore/marketing/action.html', context)
    
@login_required
def marketing_delete(request, marketing_id):
    redirect_url = 'marketing'
    try:
        marketing = Marketing.objects.get(pk=marketing_id)
    except Marketing.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                marketing = Marketing.objects.get(pk=marketing_id)
                marketing.delete()
                messages.success(request, 'Berhasil menghapus data')
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, "Gagal menghapus data")
            return redirect(redirect_url)
    else:
        context = {
            'data': marketing, 
            'url': reverse('marketing_delete', args=[marketing.id])
        }
        return render(request, 'backstore/default/delete.html', context)
    