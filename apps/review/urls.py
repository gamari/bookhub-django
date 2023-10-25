from django.urls import include, path

from apps.review import views_api

from . import views

urlpatterns = [
    path('user/<uuid:user_id>/reviews/', views.user_reviews, name='user_reviews'),
    path("review/<str:book_id>/", views.create_review, name="review_create"),

    # API
    path("api/review/<int:pk>/like/", views_api.ReviewLikeAPIView.as_view(), name="review_api"),
    path("api/review/<int:pk>/unlike/", views_api.ReviewUnLikeAPIView.as_view(), name="review_api"),
]
