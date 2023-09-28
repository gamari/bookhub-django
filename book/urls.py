from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.mypage, name="dashboard"),
    path("books/search/", views.book_search, name="book_search"),
    path("detail/<str:book_id>/", views.book_detail, name="book_detail"),

    # 本棚
    path('bookshelf/<uuid:bookshelf_id>/', views.bookshelf_list, name='bookshelf_list'),
    path('books/<int:book_id>/add_to_shelf/', views.bookshelf, name='add_to_shelf'),
    path('books/<int:book_id>/remove_from_shelf/', views.remove_from_shelf, name='remove_from_shelf'),

]
