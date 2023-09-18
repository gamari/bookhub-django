from django.urls import path

from record.views import reading_record, create_memo


urlpatterns = [
    path("reading_record/<int:book_id>/", reading_record, name="reading_record"),
    path("reading_record/<int:book_id>/memo/", create_memo, name="create_memo"),
]
