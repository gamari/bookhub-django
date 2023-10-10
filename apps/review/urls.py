from django.urls import include, path

from . import views

urlpatterns = [
    path('user/<uuid:user_id>/reviews/', views.user_reviews, name='user_reviews'),
    path("review/<str:book_id>/", views.create_review, name="review_create"),
]
