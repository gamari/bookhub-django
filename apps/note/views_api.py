import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.book.models import Book
from apps.note.domain.services import NoteDomainService

from apps.record.models import ReadingMemo

logger = logging.getLogger("app_logger")

class CreateNoteByOutput(APIView):
    def post(self, request, book_id, format=None):
        demand = request.data.get("demand", None)
        book = Book.objects.get(id=book_id)
        logger.debug(demand)
        
        # TODO とりあえず20個まで
        memos = ReadingMemo.objects.filter(user=request.user).filter(book=book).order_by("created_at")[:20]
        logger.debug(memos)
        
        service = NoteDomainService()
        content = service.create_content_by_reading_memos(memos)
        
        return Response({"content": content}, status=status.HTTP_200_OK)