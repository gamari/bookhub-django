from django.urls import path
from apps.record import views_api

from apps.record.views import (
    create_memo_api,
    mark_as_finished,
    mark_as_started,
    mark_as_unfinished,
    mark_as_unstarted,
    reading_record_page,
    memo_detail_api,
)

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
    path("api/memos/<int:memo_id>/", memo_detail_api, name="memo_detail_api"),
    path(
        "api/reading_record/<int:book_id>/memo/",
        create_memo_api,
        name="create_memo_api",
    ),
    path("api/books/<int:book_id>/memos/", views_api.GetMemoListByBookAPIView.as_view()),
]
