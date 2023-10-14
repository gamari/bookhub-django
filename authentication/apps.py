from django.apps import apps

from django.dispatch import receiver
from django.apps import AppConfig

from allauth.socialaccount.signals import pre_social_login


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"


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


@receiver(pre_social_login)
def check_social_login(request, sociallogin, **kwargs):
    print("ユーザー登録")
    print(sociallogin.account.provider)
    if sociallogin.account.provider == "google":
        data = sociallogin.account.extra_data
        email = data.get("email")
        username = data.get("name")

        if not email:
            raise ValueError("メールアドレスは必須です。")

        if not username:
            raise ValueError("ユーザー名は必須です。")

        sociallogin.user.email = email
        sociallogin.user.username = generate_unique_username(username)
    else:
        print("エラー")
        raise ValueError("Google以外のログインはできません。")
