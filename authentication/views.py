from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from authentication.application.usecases import UserDetailShowUsecase
from authentication.forms import AccountUpdateForm
from authentication.models import Account
from book.domain.repositories import BookshelfRepository


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = "pages/setting.html"
    success_url = reverse_lazy("mypage")

    def get_object(self, queryset=None):
        return self.request.user


def user_detail(request, username):
    usercase = UserDetailShowUsecase(username, BookshelfRepository())
    context = usercase.execute()
    return render(request, "pages/user_detail.html", context)


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


def contact(request):
    return render(request, "pages/contact.html")
