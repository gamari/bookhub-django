from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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
        # TODO
        pass

    return render(request, "register.html")
