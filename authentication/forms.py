from django import forms
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
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError("このユーザー名は既に使用されています。")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 4:
            raise forms.ValidationError("4文字以上を入力してください")
        return password


class AccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-input"})
        self.fields["username"].widget.attrs.update({"class": "form-input"})
        self.fields["profile_image"].widget.attrs.update({"class": "form-input-file"})

    class Meta:
        model = Account
        fields = ["email", "username", "description", "profile_image"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 1:
            raise forms.ValidationError("1文字以上を入力してください")
        return username
