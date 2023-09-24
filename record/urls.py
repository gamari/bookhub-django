from django.urls import path

from record.views import reading_record, create_memo


urlpatterns = [
    path("book/<int:book_id>/reading/", reading_record, name="reading_record"),

    # API
    path("api/reading_record/<int:book_id>/memo/", create_memo, name="create_memo"),
]
