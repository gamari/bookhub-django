from django import forms
from django.forms import ValidationError

from .models import Account


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input"}))

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 1 or len(username) > 12:
            raise ValidationError("ユーザー名は1～12文字で入力してください。")

        if Account.objects.filter(username=username).exists():
            raise ValidationError("このユーザー名は既に使用されています。")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に使用されています。")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 4:
            raise ValidationError("4文字以上を入力してください")
        return password

# TODO リファクタリングする
class AccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "max-w-sm"})
        self.fields["username"].widget.attrs.update({"class": "max-w-sm"})
        self.fields["profile_image"].widget.attrs.update({"class": "form-input-file"})

    class Meta:
        model = Account
        fields = ["email", "username", "description", "profile_image"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 1 or len(username) > 12:
            raise ValidationError("ユーザー名は1～12文字で入力してください。")

        return username
