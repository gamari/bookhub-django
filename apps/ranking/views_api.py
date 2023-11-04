import logging

from django.db.models import Count
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.book.models import Account
from apps.ranking.serializers import UserMemosRankSerializer

from apps.record.models import ReadingMemo

logger = logging.getLogger("app_logger")

class GetRankingOfMemosAPIView(APIView):
    """
    http://localhost:8000/api/ranking/books/305/memos/users/
    """
    permission_classes = [AllowAny]
    
    """対象の書籍に紐づけたメモ数の多いユーザーをランキングで返す。"""
    def get(self, request, book_id):
        user = request.user
        logger.debug(book_id)
        
        if not book_id:
            return Response("book_idを指定してください。")
        
        logger.info("user: %s, book_id: %s" % (user, book_id))
        
        # result = ReadingMemo.objects.filter(book_id=book_id).values('user').annotate(count=Count('user')).order_by('-count')[:3]
        user_counts = ReadingMemo.objects.filter(book_id=book_id) \
            .values('user') \
            .annotate(count=Count('user')) \
            .order_by('-count')[:3]

        user_ranking = {item['user']: {'count': item['count'], 'rank': i+1} 
                        for i, item in enumerate(user_counts)}

        user_ids = list(user_ranking.keys())
        users = Account.objects.filter(id__in=user_ids)

        result = []
        for user in users:
            user.rank = user_ranking[user.id]['rank']
            user.count = user_ranking[user.id]['count']
            # result.append({
            #     "user": user,
            #     "count": user.count
            # })

        sorted_result = sorted(result, key=lambda r: r['count'])
        logger.debug(sorted_result)
        
        serializer = UserMemosRankSerializer(instance=users, many=True)
        return Response(serializer.data)
        