from django.urls import path

from . import views

urlpatterns = [
    path("follow/<uuid:id>/", views.follow_account, name="follow"),
]