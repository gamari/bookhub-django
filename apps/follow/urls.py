from django.urls import path

from apps.follow import api_views

from . import views

urlpatterns = [
    path(
        "accounts/<uuid:id>/follower/", views.show_follower_page, name="follower_page"
    ),
    path("follow/<uuid:id>/", views.follow_account, name="follow"),
    path("unfollow/<uuid:id>/", views.unfollow_account, name="unfollow"),

    path("api/follow/<uuid:id>/", api_views.follow_api, name="api_follow"),
    path("api/unfollow/<uuid:id>/", api_views.unfollow_api, name="api_unfollow"),
]
