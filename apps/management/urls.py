from django.urls import path

from . import views

urlpatterns = [
    path('manage/dashboard/', views.management_dashboard, name='management_dashboard'),
]