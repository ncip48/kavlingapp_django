from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from .forms import *
from django.views import generic
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import *
import re
from django_serverside_datatable.views import ServerSideDatatableView
from django_serverside_datatable import datatable


# Create your views here.

#auth
def login_view(request):
    print(User.objects.all())
    next = ""
    if request.GET:  
        next = request.GET['next']
    
    if next != "":
        action = "?next=" + next
    else:
        action = ''
        
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            check = User.objects.get(username=username)
        except:
            messages.error(request, "Akun tidak ditemukan")
            return redirect(action)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next == "":
                return redirect('dashboard')
            else:
                return redirect(next)
        else:
            messages.error(request, "Username atau password salah")
        
    return render(request, "backstore/login.html", {'action':action})

def logout_view(request):
    logout(request)
    return redirect('login/')

# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
# @permission_required('dashboard.index')
def svg(request):
    return render(request, 'svg_editor/index.html')

@login_required
# @permission_required('dashboard.index')
def dashboard(request):
    return render(request, 'backstore/dashboard.html')

@login_required
def add_permission(request):
    user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            is_staff=1,
            is_superuser=0,
        )
    permission = Permission.objects.get(name='Can view excel data')
    user.user_permissions.add(permission)
    user.save()

@login_required
# @permission_required('catalog.awokwok', raise_exception=True)
def user_index(request):
    context = {
        'title': 'User',
        'datas': User.objects.all()
    }
    return render(request, 'backstore/user/index.html', context)

# class ListUserView(ServerSideDatatableView):
# 	queryset = User.objects.all()
# 	columns = ['username', 'email', 'full_name']

def user_list(request, *args, **kwargs):
    datas = User.objects.all()
    columns = ['id', 'username', 'email', 'first_name', 'last_name','is_staff']
    result = datatable.DataTablesServer(
        request, columns, datas
    ).output_result()
    return JsonResponse(result, safe=False)

@login_required
def user_create(request):
    redirect_url = 'user'
    if request.POST:
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email sudah terdaftar')
            return redirect(redirect_url)
        try:
            with transaction.atomic():
                form = UserForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    messages.success(request, "Berhasil menambahkan data")
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, f"Gagal menambahkan data {e}")
            return redirect(redirect_url)
    else:
        form = UserForm()
        form.fields['password'].required = True
        context = {
            'form': form
        }
        return render(request, 'backstore/user/action.html', context)

@login_required
def user_update(request, user_id):
    redirect_url = 'user'
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                form = UserForm(request.POST, instance=user)
                if form.is_valid():
                    if request.POST.get('password') != '':
                        new_password= form.cleaned_data['password']
                        user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Berhasil mengubah data')
                    return redirect(redirect_url)
                else:
                    messages.error(request, "Data tidak valid")
                    return redirect(redirect_url)
        except Exception as e:
            messages.error(request, "Gagal mengedit data")
            return redirect(redirect_url)
    else:
        form = UserForm(instance=user)
        form.fields['password'].required = False
        context = {
            'form': form, 
            'data': user
        }
        return render(request, 'backstore/user/action.html', context)
    
@login_required
def user_delete(request, user_id):
    redirect_url = 'user'
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Data tidak ditemukan"})
    if request.POST:
        try:
            with transaction.atomic():
                user = User.objects.get(pk=user_id)
                user.delete()
                messages.success(request, 'Berhasil menghapus data')
                return redirect(redirect_url)
        except Exception as e:
            messages.error(request, "Gagal menghapus data")
            return redirect(redirect_url)
    else:
        context = {
            'data': user, 
            'url': reverse('user_delete', args=[user.id])
        }
        return render(request, 'backstore/default/delete.html', context)

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