from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from authentication.models import Account


def account_detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, 'account_detail.html', {'account': account})


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

@login_required
def show_setting(request):
    return render(request, 'setting.html')