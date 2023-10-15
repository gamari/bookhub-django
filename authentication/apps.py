from django.apps import apps

from django.dispatch import receiver
from django.apps import AppConfig

from allauth.socialaccount.signals import pre_social_login


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"


# TODO リファクタリングしたい
def generate_unique_username(base_username):
    Account = apps.get_model("authentication", "Account")

    if not Account.objects.filter(username=base_username).exists():
        return base_username

    counter = 1
    new_username = f"{base_username}{counter}"
    while Account.objects.filter(username=new_username).exists():
        counter += 1
        new_username = f"{base_username}{counter}"

    return new_username

def check_duplicate_email(email):
    Account = apps.get_model("authentication", "Account")
    if Account.objects.filter(email=email).exists():
        return True
    else:
        return False


@receiver(pre_social_login)
def check_social_login(request, sociallogin, **kwargs):
    if sociallogin.account.provider == "google":
        if sociallogin.is_existing:
            return

        data = sociallogin.account.extra_data
        email = data.get("email")
        username = data.get("name")

        if not email:
            raise ValueError("メールアドレスは必須です。")
        
        # emailチェック
        if check_duplicate_email(email):
            raise ValueError("このメールアドレスは既に登録されています。")

        if not username:
            raise ValueError("ユーザー名は必須です。")

        sociallogin.user.email = email
        sociallogin.user.username = generate_unique_username(username)
    else:
        print("エラー")
        raise ValueError("Google以外のログインはできません。")
