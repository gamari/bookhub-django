import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.book.serializers import BookSerializer
from apps.search.application.usecases import BookSearchByTitleUsecase

from apps.search.domain.services import BookSearchService

logger = logging.getLogger("app_logger")

class SearchBookAPIView(APIView):
    """
    書籍検索API

    テスト用パラメータ
    {"query": "java", "page": 1}
    
    """
    
    def post(self, request, format=None):
        query = request.data.get("query")
        page = int(request.data.get("page", 1))
        mode = ""
        
        try:
            search_service = BookSearchService()
            usecase = BookSearchByTitleUsecase(search_service)
            context = usecase.execute(mode, page, query)
            logger.debug(context)
            serializer = BookSerializer(context["results"], many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(e)
            return Response({"message": "error"}, status=400)
