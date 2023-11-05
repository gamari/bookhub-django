from django.urls import path
from apps.record import views_api

from apps.record.views import (
    mark_as_finished,
    mark_as_started,
    mark_as_unfinished,
    mark_as_unstarted,
    reading_record_page,
)
from apps.record.views_api import CreateMemoAPI, GetMemoListByFollowingUsersAPIView,  memo_delete_api

urlpatterns = [
    path("book/<int:book_id>/reading/", reading_record_page, name="reading_record"),
    path("mark_as_started/<int:book_id>/", mark_as_started, name="mark_as_started"),
    path(
        "mark_as_unstarted/<int:book_id>/", mark_as_unstarted, name="mark_as_unstarted"
    ),
    path("mark_as_finished/<int:book_id>/", mark_as_finished, name="mark_as_finished"),
    path(
        "mark_as_unfinished/<int:book_id>/",
        mark_as_unfinished,
        name="mark_as_unfinished",
    ),
    # API
    path("api/users/<uuid:user_id>/memos/", views_api.GetMemoListByUserAPIView.as_view()),
    
    path("api/memos/<int:memo_id>/", memo_delete_api, name="memo_detail_api"),
    path(
        "api/reading_record/<int:book_id>/memo/",
        CreateMemoAPI.as_view(),
        name="create_memo_api",
    ),
    path("api/books/<int:book_id>/memos/", views_api.GetMemoListByBookAPIView.as_view()),
    path("api/followings/memos/", GetMemoListByFollowingUsersAPIView.as_view()),
]
