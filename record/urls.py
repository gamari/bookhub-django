from django.urls import path

from record.views import (
    mark_as_finished,
    mark_as_started,
    mark_as_unfinished,
    mark_as_unstarted,
    reading_record,
    create_memo,
)

urlpatterns = [
    path("book/<int:book_id>/reading/", reading_record, name="reading_record"),
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
    path("api/reading_record/<int:book_id>/memo/", create_memo, name="create_memo"),
]
