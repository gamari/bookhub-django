from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_home, name="home"),
    path("dashboard/", views.show_dashboard, name="dashboard"),
    path("books/search/", views.show_book_search, name="book_search"),
    path("detail/<str:book_id>/", views.show_book_detail, name="book_detail"),
    path('books/<int:book_id>/add_to_shelf/', views.add_to_shelf, name='add_to_shelf'),
    path('books/<int:book_id>/remove_from_shelf/', views.remove_from_shelf, name='remove_from_shelf'),

]
