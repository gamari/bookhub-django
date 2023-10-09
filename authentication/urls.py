from django.urls import path
from . import views

urlpatterns = [
    path("user/<str:username>/", views.user_detail, name="user_detail"),
    path(
        "setting/delete_profile_image/",
        views.delete_profile_image,
        name="delete_profile_image",
    ),
    path("setting/", views.AccountUpdateView.as_view(), name="setting"),
    # 認証関係
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
