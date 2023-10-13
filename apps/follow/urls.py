from django.urls import path

from apps.follow import api_views

from . import views

urlpatterns = [
    path(
        "accounts/<uuid:id>/follower/", views.show_follower_page, name="follower_page"
    ),
    path(
        "accounts/<uuid:id>/following/", views.show_following_page, name="following_page"
    ),

    # API
    path("api/follow/<uuid:id>/", api_views.follow_api, name="api_follow"),
    path("api/unfollow/<uuid:id>/", api_views.unfollow_api, name="api_unfollow"),
]
