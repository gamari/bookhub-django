from django.urls import include, path

from . import views

urlpatterns = [
    path("review/<str:book_id>/", views.create_review, name="review_create"),
]
