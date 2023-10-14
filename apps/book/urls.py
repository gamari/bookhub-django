from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mypage/", views.mypage, name="mypage"),
    path("detail/<str:book_id>/", views.book_detail_page, name="book_detail"),
    path("selection/create/", views.create_selection, name="create_selection"),
    path("selection/<uuid:selection_id>/", views.selection_detail, name="selection_detail"),

    # 本棚
    path('bookshelf/<uuid:bookshelf_id>/', views.bookshelf_list_page, name='bookshelf_list'),
    path('books/<int:book_id>/add_to_shelf/', views.add_book_to_shelf, name='add_to_shelf'),
    path('books/<int:book_id>/remove_from_shelf/', views.remove_book_from_shelf, name='remove_from_shelf'),

]
