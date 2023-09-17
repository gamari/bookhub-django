from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_home, name="home"),
    path("dashboard/", views.show_dashboard, name="dashboard"),
    path("books/search/", views.show_book_search, name="book_search"),
    path("detail/<str:book_id>/", views.book_detail, name="book_detail"),
]
