from django.contrib.auth.models import User, Permission
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from .forms import *

# Create your views here.

#auth
def login_view(request):
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
@permission_required('dashboard.index')
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

@login_required
def user_create(request):
    if request.POST:
        try:
            id = request.POST.get("id")
            with transaction.atomic():
                form = UserForm(request.POST)
                # Mengecek validasi form
                if form.is_valid():
                    # Membuat Task baru dengan data yang disubmit
                    new_user = UserForm(request.POST)
                    # Simpan data ke dalam table tasks
                    new_user.save()
            messages.success(request, "Berhasil menambahkan data")
            return redirect('user')
        except Exception as e:
            messages.error(request, "Gagal menambahkan data")
            return redirect('user')
    else:
        form = UserForm()
        return render(request, 'backstore/user/action.html', {'form': form})

@login_required
def user_update(request, user_id):
    try:
        # mengambil data task yang akan diubah berdasarkan task id
        task = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Jika data task tidak ditemukan,
        # maka akan di redirect ke halaman 404 (Page not found).
        raise Http404("Task tidak ditemukan.")
    # Mengecek method pada request
    # Jika method-nya adalah POST, maka akan dijalankan
    # proses validasi dan penyimpanan data
    if request.method == 'POST':
        form = UserForm(request.POST, instance=task)
        if form.is_valid():
            # Simpan perubahan data ke dalam table tasks
            form.save()
            # mengeset pesan sukses dan redirect ke halaman daftar task
            messages.success(request, 'Sukses Mengubah Task.')
            return redirect('user')
    # Jika method-nya bukan POST
    else:
        # membuat objek dari class TaskForm
        form = UserForm(instance=task)
    # merender template form dengan memparsing data form
    return render(request, 'backstore/user/action.html', {'form': form})