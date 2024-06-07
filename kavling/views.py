from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#auth
def login_view(request):
    next = ""
    if request.GET:  
        next = request.GET['next']
    
    if next != "":
        action = "signin" + "?next=" + next
    else:
        action = 'signin'
        
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
        
    return render(request, "login.html", {'action':action})

@login_required
def dashboard(request):
    return render(request, 'empty/index.html',)