from django.shortcuts import render, redirect
from customer.models import Customer
from customer.forms import CustomerForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from kavling.functions.functions import handle_uploaded_file
# Create your views here.

@login_required
# @permission_required('catalog.awokwok', raise_exception=True)
def customer_index(request):
    context = {
        'title': 'Customer',
        'datas': Customer.objects.all(),
    }
    return render(request, 'backstore/customer/index.html', context)

@login_required
def customer_create(request):
    redirect_url = 'customer'
    if request.POST:
        try:
            with transaction.atomic():
                form = CustomerForm(request.POST)
                if form.is_valid():
                    customer = form.save(commit=False)
                    if 'ktp' in request.FILES:
                        ktp = handle_uploaded_file(request.FILES['ktp'])
                        customer.ktp = ktp
                    if 'kk' in request.FILES:
                        kk = handle_uploaded_file(request.FILES['kk'])  
                        customer.kk = kk
                    customer.save()
                    messages.success(request, "Berhasil menambahkan data")
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal menambahkan data {e}")
            return redirect(redirect_url)
    else:
        form = CustomerForm()
        context = {
            'form': form
        }
        return render(request, 'backstore/customer/action.html', context)
    
@login_required
def customer_update(request, customer_id):
    redirect_url = 'customer'
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                form = CustomerForm(request.POST, instance=customer)
                if form.is_valid():
                    if 'ktp' in request.FILES:
                        ktp = handle_uploaded_file(request.FILES['ktp'])
                        customer.ktp = ktp
                    if 'kk' in request.FILES:
                        kk = handle_uploaded_file(request.FILES['kk'])  
                        customer.kk = kk
                    customer.save()
                    messages.success(request, 'Berhasil mengubah data')
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal mengedit data {e}")
            return redirect(redirect_url)
    else:
        form = CustomerForm(instance=customer)
        context = {
            'form': form, 
            'data': customer
        }
        return render(request, 'backstore/customer/action.html', context)
    
@login_required
def customer_delete(request, customer_id):
    redirect_url = 'customer'
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                customer = Customer.objects.get(pk=customer_id)
                customer.delete()
                messages.success(request, 'Berhasil menghapus data')
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, "Gagal menghapus data")
            return redirect(redirect_url)
    else:
        context = {
            'data': customer, 
            'url': reverse('customer_delete', args=[customer.id])
        }
        return render(request, 'backstore/default/delete.html', context)
    