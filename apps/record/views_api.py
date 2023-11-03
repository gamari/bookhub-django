import logging

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.record.domain.services import MemoDomainService
from .models import ReadingMemo
from .serializers import ReadingMemoSerializer

logger = logging.getLogger("app_logger")


class GetMemoListByBookAPIView(APIView):
    def get(self, request, book_id):
        page = request.query_params.get("page")
        is_all = request.query_params.get("is_all")
        since_date = request.query_params.get("since_date")
        previous_date = request.query_params.get("previous_date")

        logger.debug(previous_date)
        logger.debug(is_all)

        service = MemoDomainService.initialize()
        if previous_date:
            if is_all:
                memos = service.get_memos_by_book_and_date(
                    book_id, previous_date, limit=10
                )
            else:
                memos = service.get_memos_by_book_and_date_and_user(
                    book_id, previous_date, request.user, limit=10
                )
        else:
            # memos = service.get_memos_of_book_with_paginate(book_id, page)
            memos = []

        logger.info(memos)

        serializer = ReadingMemoSerializer(memos, many=True)
        return Response(serializer.data)
