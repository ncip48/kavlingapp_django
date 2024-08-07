from django.shortcuts import render, redirect
from user.models import User
from user.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.models import Permission

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