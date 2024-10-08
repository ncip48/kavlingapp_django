from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from kavling.models import Kavling
from website.models import Site
from transaksi.forms import *
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import locale
locale.setlocale(locale.LC_ALL, "")
from datetime import datetime
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.templatetags.static import static
from datetime import datetime
# import locale
# for German locale
# locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

# Create your views here.
@login_required
def transaksi_index(request):
    context = {
        'kavlings': Kavling.objects.all(),
        'kavling': Site.objects.get(pk=1),
        'title': 'Transaksi'
    }
    return render(request, 'backstore/transaksi/index.html', context)

@login_required
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

@login_required
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
def transaksi_update(request, transaksi_id):
    redirect_url = 'penjualan'
    try:
        transaksi = Transaksi.objects.get(pk=transaksi_id)
    except Transaksi.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                    if request.POST.get('tipe_transaksi') == "1":
                        transaksi.pembayaran_cash = request.POST['pembayaran_cash']
                        transaksi.is_lunas = 1
                        transaksi.tipe_transaksi = 1
                        
                        kavling = transaksi.kavling
                        kavling.status = 2
                        kavling.save()
                    elif request.POST.get('tipe_transaksi') == "2":
                        transaksi.dp = request.POST['dp']
                        transaksi.tenor = request.POST['tenor']
                        transaksi.cicilan_per_bulan = request.POST['cicilan_per_bulan']
                        transaksi.tanggal_tempo = request.POST['tanggal_tempo']
                        transaksi.tipe_transaksi = 2
                        transaksi.is_lunas = 0
                        
                        kavling = transaksi.kavling
                        kavling.status = 2
                        kavling.save()
                    
                    transaksi.keterangan = request.POST['keterangan']
                    transaksi.pembelian_booking = None
                    transaksi.save()
                    messages.success(request, "Berhasil mengupdate transaksi")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal mengupdate transasksi {e}")
            return redirect(redirect_url)
        
@login_required
def penjualan_index(request):
    # Get the user's role
    role = request.user.role

    # Base context dictionary
    context = {
        'title': 'Penjualan',
    }

    # Filter 'datas' based on role
    if role == 1:
        # Assuming 'marketing_id' is a field in the 'Transaksi' model
        context['datas'] = Transaksi.objects.filter(marketing_id=request.user.id)
    else:
        # Default behavior for other roles
        context['datas'] = Transaksi.objects.all()
        
    return render(request, 'backstore/penjualan/index.html', context)

@login_required
def penjualan_detail(request, unique_id):
    trx = Transaksi.objects.get(unique_id=unique_id)
    
    tenor_range = range(trx.tenor) if trx.tenor is not None else []
    
    context = {
        'data': trx,
        'title': 'Detail Penjualan',
        'form': TransaksiFormReadOnly(instance=trx),
        'form_cash': TransaksiFormCash(),
        'form_kredit': TransaksiFormKredit(),
        'tenor': tenor_range,
    }
    return render(request, 'backstore/penjualan/detail.html', context)

@login_required
def penjualan_delete(request, transaksi_id):
    redirect_url = 'penjualan'
    try:
        transaksi = Transaksi.objects.get(pk=transaksi_id)
    except Transaksi.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                transaksi = Transaksi.objects.get(pk=transaksi_id)
                
                #update kavling
                kavling = Kavling.objects.get(pk=transaksi.kavling_id)
                kavling.status = 0
                kavling.save()
                transaksi.delete()
                messages.success(request, 'Berhasil menghapus data')
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal menghapus data {e}")
            return redirect(redirect_url)
    else:
        context = {
            'data': transaksi, 
        'url': reverse('penjualan_delete', args=[transaksi.id])
        }
        return render(request, 'backstore/default/delete.html', context)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)  # Use UTF-8 encoding
    if pdf.err:
        return HttpResponse("Invalid PDF", status=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

def rupiah_format(uang):
    y = str(uang)
    if len(y) <= 3 :
        return 'Rp ' + y     
    else :
        p = y[-3:]
        q = y[:-3]
        return   rupiah_format(q) + '.' + p

@login_required
def generate_kwitansi(request, unique_id):
    trx = Transaksi.objects.get(unique_id=unique_id)
    invoice_number = f'kwitansi_{trx.unique_id}'
    
    date_obj = trx.tanggal_transaksi
    
    if trx.tipe_transaksi == 0:
        nominal = trx.pembelian_booking
    elif trx.tipe_transaksi == 1:
        nominal = trx.pembayaran_cash
    elif trx.tipe_transaksi == 2:
        nominal = trx.dp
    
    context = {
        "transaksi": trx,
        "nominal":rupiah_format(nominal),
        "date": date_obj.strftime("%d %B %Y"),
        "terbilang": trx.terbilang
    }
    
    # return render(request, 'pdf/invoice.html', context)
    
    response = render_to_pdf("pdf/invoice.html", context)
    filename = f"Invoice_{invoice_number}.pdf"
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response

@login_required
def generate_kwitansi_cicilan(request, unique_id):
    cicilan = Cicilan.objects.get(unique_id=unique_id)
    invoice_number = f'kwitansi_{cicilan.unique_id}'
    
    date_obj = cicilan.tanggal_pembayaran
    
    context = {
        "transaksi": cicilan,
        "nominal":rupiah_format(cicilan.nominal),
        "date": date_obj.strftime("%d %B %Y"),
        "terbilang": cicilan.terbilang
    }
    
    # return render(request, 'pdf/invoice.html', context)
    
    response = render_to_pdf("pdf/cicilan.html", context)
    filename = f"Invoice_{invoice_number}.pdf"
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response

@login_required
def cicilan_pdf(request, unique_id):
    invoice_number = "007cae"
    transaksi = Transaksi.objects.get(unique_id=unique_id);
    cicilan = Cicilan.objects.filter(transaksi=transaksi)
    
    now = datetime.now()
    
    context = {
        "transaksi": transaksi,
        "datas": cicilan,
        "date": now.strftime("%d %B %Y"),
    }
    
    # return render(request, 'pdf/total_cicilan.html', context)
    
    response = render_to_pdf("pdf/total_cicilan.html", context)
    filename = f"Invoice_{invoice_number}.pdf"
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response

@login_required
def generate_pdf(request):
    invoice_number = "007cae"
    now = datetime.now()
    context = {
        "bill_to": "Ethan Hunt",
        "invoice_number": f"{invoice_number}",
        "amount": locale.currency(100_000, grouping=True),
        "date": "2021-07-04",
        "pdf_title": f"Invoice #{invoice_number}",
        "bgpdf": static('images/kwitansi.pdf'),
        "date": now.strftime("%d %B %Y")
    }
    
    # return render(request, 'pdf/invoice.html', context)
    
    response = render_to_pdf("pdf/invoice.html", context)
    filename = f"Invoice_{invoice_number}.pdf"
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response

@login_required
def cicilan_create(request, transaksi_id):
    try:
        transaksi = Transaksi.objects.get(pk=transaksi_id)
        redirect_url = f'/panel/penjualan/{transaksi.unique_id}'
    except Transaksi.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                pembayaran_ke = request.POST.get('pembayaran_ke')
                nominal = transaksi.cicilan_per_bulan
                current_date = datetime.now().date()
                
                
                # Check if cicilan already exists
                cicilan, created = Cicilan.objects.update_or_create(
                    transaksi=transaksi,
                    pembayaran_ke=pembayaran_ke,
                    nominal=nominal,
                    tanggal_pembayaran=current_date
                )
                
                if pembayaran_ke == "1":
                    transaksi.pembayaran_cash = transaksi.cicilan_per_bulan + transaksi.dp
                else:
                    # Ensure that transaksi.pembayaran_cash is initialized if it's not already set
                    transaksi.pembayaran_cash += transaksi.cicilan_per_bulan
                
                pmb = int(pembayaran_ke)
                if pmb == int(transaksi.tenor):
                    transaksi.is_lunas = 1
                
                transaksi.save()
                messages.success(request, "Berhasil membayar cicilan")
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal membayar cicilan {e}")
            return redirect(redirect_url)