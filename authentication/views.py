from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from authentication.forms import AccountUpdateForm
from authentication.models import Account


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = "setting.html"
    success_url = reverse_lazy("mypage")

    def get_object(self, queryset=None):
        return self.request.user


def user_detail(request, username):
    user = get_object_or_404(Account, username=username)
    return render(request, "user_detail.html", {"user": user})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect("mypage")
        else:
            return render(request, "login.html", {"error": "メールアドレスまたはパスワードが間違っています。"})

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = Account.objects.create_user(
            email=email, password=password, username=username
        )
        if user:
            login(request, user)
            return redirect("mypage")
        else:
            return render(request, "register.html", {"error": "Registration failed"})

    return render(request, "register.html")


def logout_view(request):
    print("logoutします")
    logout(request)
    return redirect("login")


@login_required
def show_setting(request):
    return render(request, "setting.html")
