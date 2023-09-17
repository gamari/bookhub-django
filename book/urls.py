from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.show_dashboard, name="dashboard"),
]