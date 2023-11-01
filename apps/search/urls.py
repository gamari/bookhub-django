from django.urls import path

from . import views, views_api

urlpatterns = [
    path("books/search/", views.book_search, name="book_search"),
    path("book/search/tag/", views.tag_search, name="book_search_by_tag"),

    path("api/books/search/", views_api.SearchBookAPIView.as_view(), name="api_book_search"),
]
