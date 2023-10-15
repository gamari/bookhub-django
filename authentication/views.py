from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from authentication.application.usecases import UserDetailShowUsecase
from authentication.forms import AccountUpdateForm, LoginForm, RegisterForm
from authentication.models import Account

from apps.book.domain.repositories import BookshelfRepository


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = "pages/setting.html"
    success_url = reverse_lazy("mypage")

    def get_object(self, queryset=None):
        return self.request.user


def delete_profile_image(request):
    if request.method != "POST":
        # TODO エラー処理する
        return redirect("setting")
    user = request.user
    user.profile_image = None
    user.save()
    return redirect("setting")


def user_detail(request, username):
    usercase = UserDetailShowUsecase(username, request.user, BookshelfRepository())
    context = usercase.execute()
    return render(request, "pages/user_detail.html", context)


def login_view(request):
    error_message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("mypage")
            else:
                error_message = "メールアドレスまたはパスワードが間違っています。"
    else:
        form = LoginForm()
    return render(request, "pages/login.html", {"form": form, "error": error_message})


def register_view(request):
    error_message = ""
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = form.cleaned_data.get("username")

            user = Account.objects.create_user(
                email=email, password=password, username=username
            )

            if user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect("mypage")
            else:
                error_message = "ユーザー登録に失敗しました。"
    else:
        form = RegisterForm()

    return render(request, "pages/register.html", {"form": form, "error": error_message})


def logout_view(request):
    logout(request)
    return redirect("login")
