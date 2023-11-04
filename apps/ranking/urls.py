from django.urls import path
from apps.ranking.views_api import GetRankingOfMemosAPIView


urlpatterns = [
    path("api/ranking/books/<int:book_id>/memos/users/", GetRankingOfMemosAPIView.as_view(), name="api-ranking-books-memos-users"),
]
