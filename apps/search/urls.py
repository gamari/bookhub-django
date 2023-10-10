from django.urls import path

from . import views

urlpatterns = [
    path("books/search/", views.book_search, name="book_search"),
]
