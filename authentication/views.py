from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from authentication.models import Account

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'メールアドレスまたはパスワードが間違っています。'})

    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        user = Account.objects.create_user(email=email, password=password, username=username)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'register.html', {'error': 'Registration failed'})


    return render(request, "register.html")

def logout_view(request):
    print("logoutします")
    logout(request)
    return redirect("login")
