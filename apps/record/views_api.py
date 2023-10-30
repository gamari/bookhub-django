from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.record.domain.services import MemoDomainService
from .models import ReadingMemo
from .serializers import ReadingMemoSerializer

class ReadingMemoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReadingMemo.objects.all()
    serializer_class = ReadingMemoSerializer

    def list(self, request, *args, **kwargs):
        since_date = request.query_params.get('since_date')
        previous_date = request.query_params.get('previous_date')

        service = MemoDomainService.initialize()

        memos = service.get_memos_of_followings_and_me(request.user, limit=1, since_date=since_date, previous_date=previous_date)

        serializer = self.get_serializer(memos, many=True)
        return Response(serializer.data)

class GetMemoListByBookAPIView(APIView):
    def get(self, request, book_id):
        page = request.query_params.get('page')

        service = MemoDomainService.initialize()
        memos = service.get_memos_of_book_with_paginate(book_id, page)

        serializer = ReadingMemoSerializer(memos, many=True)
        return Response(serializer.data)