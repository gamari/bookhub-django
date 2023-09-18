from django.urls import path

from record.views import reading_record


urlpatterns = [
    path("reading_record/<int:book_id>/", reading_record, name="reading_record"),
]
