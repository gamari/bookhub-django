from django.urls import path

from . import views

urlpatterns = [
    path("accounts/<uuid:id>/follower/", views.follower_page, name="follower_page"),

    path("follow/<uuid:id>/", views.follow_account, name="follow"),
    path("unfollow/<uuid:id>/", views.unfollow_account, name="unfollow"),
]