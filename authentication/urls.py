from django.urls import path
from . import views

urlpatterns = [
    path('account/<str:username>/', views.account_detail, name='account_detail'),

    path('login/', views.login_view, name='login'),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("setting/", views.AccountUpdateView.as_view(), name="setting"),
]
