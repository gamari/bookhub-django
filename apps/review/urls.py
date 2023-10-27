from django.urls import path

from apps.review import views_api

from . import views

urlpatterns = [
    path('user/<uuid:user_id>/reviews/', views.user_reviews, name='user_reviews'),

    # API
    path("api/books/<str:book_id>/review/", views_api.ReviewDetailAPIView.as_view(), name="api_review_detail"),

    path("api/review/<int:pk>/like/", views_api.ReviewLikeAPIView.as_view()),
    path("api/review/<int:pk>/unlike/", views_api.ReviewUnLikeAPIView.as_view()),
]
