from django.urls import path

from . import views, views_api

urlpatterns = [
    path('manage/dashboard/', views.management_dashboard, name='management_dashboard'),
    path('manage/books/', views.management_books, name='management_books'),
    path("manage/book/duplicate/", views.management_duplicate_books, name="management_book_duplicate"),
    path('manage/book/<int:book_id>/', views.management_book_edit, name='management_book_edit'),
    path('manage/book/<int:book_id>/delete/', views.management_delete_book, name='management_book_delete'),
    path('manage/books/<int:source_id>/merge/<int:target_id>/', views.management_book_merge, name='management_book_merge'),
    path('manage/contacts/', views.management_contacts, name='management_contacts'),
    path('manage/search-history/', views.management_search_history, name='management_search_history'),
    path('manage/notices/', views.management_notices, name='management_notices'),
    path('manage/notice/create/', views.management_notice_create, name='management_notice_create'),
    path('manage/notice/<int:notice_id>/edit/', views.management_notice_edit, name='management_notice_edit'),
    path('manage/notice/<int:notice_id>/delete/', views.management_notice_delete, name='management_notice_delete'),
    path('manage/ai-users/', views.management_ai_users, name='management_ai_users'),
    path('manage/ai-user/<uuid:user_id>/', views.management_ai_users_edit, name='management_ai_users_edit'),
    path("api/manage/post/recommend/", views_api.RecommendPostAPIView.as_view(), name="management_post_recommend"),
]