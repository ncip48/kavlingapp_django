from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *
from django.urls import reverse
from .models import *
import re


# Create your views here.
# custom 404 view
def custom_404(request, exception):
    # return render(request, '404.html', status=404)
    return redirect('dashboard')

@login_required
# @permission_required('dashboard.index')
def svg(request):
    return render(request, 'svg_editor/index.html')

@login_required
# @permission_required('catalog.awokwok', raise_exception=True)
def kavling_index(request):
    context = {
        'title': 'Kavling',
        'datas': Kavling.objects.all(),
        'kavling': Site.objects.first(),
    }
    return render(request, 'backstore/kavling/index.html', context)

@login_required
def kavling_create(request):
    redirect_url = 'kavling'
    if request.POST:
        try:
            with transaction.atomic():
                form = KavlingForm(request.POST)
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
        form = KavlingForm()
        context = {
            'form': form
        }
        return render(request, 'backstore/kavling/action.html', context)
    
@login_required
def kavling_import(request):
    redirect_url = 'kavling'
    if request.POST:
        kode = request.POST['kode']
        split_kode = re.findall(r'<g.*?</g>', kode, re.DOTALL)
        try:
            with transaction.atomic():
                for index, res in enumerate(split_kode):
                    # print(res)
                    # print(split_text[index])
                    g_first = re.search(r'<g[^>]*>', res).group()
                    # print(g_first)
                    pattern = r'<g[^>]*>((?:(?!<g)[\s\S])*?)</g>'
                    matches = re.findall(pattern, res)
                    x = g_first + ''.join(matches) + '</g>'
                    # print(x)
                    code = re.search(r'<g.*?>', x).group()
                    path = re.search(r'<path[^>]*/>', x).group()
                    path = re.search(r'd="([^"]+)"', path).group(1)
                    # print(code)
                    # print(path)
                    text = re.search(r'<text[^>]*', x).group()
                    if '<tspan' in x:
                        text = re.search(r'<tspan[^>]*', x).group()
                        text_match = re.search(r'<tspan.*?>([^<]+)</tspan>', x)
                        if text_match:
                            kode_kavling = text_match.group(1)
                    else:
                        text = text
                        text_match = re.search(r'<text.*?>([^<]+)</text>', x)
                        if text_match:
                            kode_kavling = text_match.group(1)
                    text_x = re.search(r' x="([^"]+)"', text).group()
                    text_y = re.search(r' y="([^"]+)"', text).group()
                    check_transform = re.search(r'transform="([^"]+)"', text)
                    check_fs = re.search(r'font-size="([^"]+)"', text)
                    if check_transform:
                        text_transform = check_transform.group()
                    else:
                        text_transform = ''
                    if check_fs:
                        font_size = check_fs.group()
                    else:
                        font_size = ''
                    text = f"{text_x} {text_y} {text_transform} {font_size}"
                    # print(text)
                    # print(text_x, text_y, kode_kavling)
                    kavling = Kavling(
                        kode_kavling=kode_kavling,
                        map_code_g=code,
                        map_code_path=path,
                        text_code_svg=text,
                        luas_tanah=0,
                        harga_per_meter=0,
                        harga_jual_cash=0,   
                    )
                    kavling.save()
                messages.success(request, "Berhasil menambahkan data")
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal menambahkan data {e}")
            return redirect(redirect_url)
    else:
        form = KavlingForm()
        context = {
            'form': form
        }
        return render(request, 'backstore/kavling/import.html', context)
    
@login_required
def kavling_template(request):
    redirect_url = 'kavling'
    site = Site.objects.get(pk=1)
    if request.POST:
        try:
            with transaction.atomic():
                form = TemplateKavlingForm(request.POST, instance=site)
                site = form.save(commit=False)
                code = re.search(r'<svg.*?>', request.POST['template_kavling']).group()
                site.placement_template = code
                site.save()
                messages.success(request, "Berhasil merubah data")
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal menambahkan data {e}")
            return redirect(redirect_url)
    else:
        form = TemplateKavlingForm(instance=site)
        context = {
            'form': form
        }
        return render(request, 'backstore/kavling/template.html', context)

@login_required
def kavling_update(request, kavling_id):
    redirect_url = 'kavling'
    try:
        kavling = Kavling.objects.get(pk=kavling_id)
    except Kavling.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                form = KavlingForm(request.POST, instance=kavling)
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
        form = KavlingForm(instance=kavling)
        context = {
            'form': form, 
            'data': kavling
        }
        return render(request, 'backstore/kavling/action.html', context)
    
@login_required
def kavling_delete(request, kavling_id):
    redirect_url = 'kavling'
    try:
        kavling = Kavling.objects.get(pk=kavling_id)
    except Kavling.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                kavling = Kavling.objects.get(pk=kavling_id)
                kavling.delete()
                messages.success(request, 'Berhasil menghapus data')
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, "Gagal menghapus data")
            return redirect(redirect_url)
    else:
        context = {
            'data': kavling, 
            'url': reverse('kavling_delete', args=[kavling.id])
        }
        return render(request, 'backstore/default/delete.html', context)
    
@login_required
def kavling_detail(request, kavling_id):
    try:
        kavling = Kavling.objects.get(pk=kavling_id)
    except Kavling.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    
    context = {
        'form': DetailKavlingForm(instance=kavling),
        'data': kavling
    }
    return render(request, 'backstore/kavling/detail.html', context)