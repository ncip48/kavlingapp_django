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

from xhtml2pdf import pisa

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
    context = {
        'datas': Transaksi.objects.all(),
        'title': 'Penjualan'
    }
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
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

@login_required
def generate_pdf(request):
    invoice_number = "007cae"
    context = {
        "bill_to": "Ethan Hunt",
        "invoice_number": f"{invoice_number}",
        "amount": locale.currency(100_000, grouping=True),
        "date": "2021-07-04",
        "pdf_title": f"Invoice #{invoice_number}",
    }
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