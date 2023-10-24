from django.urls import path

from . import views

urlpatterns = [
    path('manage/dashboard/', views.management_dashboard, name='management_dashboard'),
    path('manage/books/', views.management_books, name='management_books'),
    path('manage/book/<int:book_id>/', views.management_book_edit, name='management_book_edit'),
    path('manage/contacts/', views.management_contacts, name='management_contacts'),
    path('manage/search-history/', views.management_search_history, name='management_search_history'),
]