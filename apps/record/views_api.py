import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from apps.record.application.usecases import CreateMemoUsecase, DeleteMemoUsecase
from apps.record.domain.repositories import ReadingMemoRepository

from apps.record.domain.services import MemoDomainService
from .serializers import ReadingMemoSerializer

logger = logging.getLogger("app_logger")

class GetMemoListByUserAPIView(APIView):
    def get(self, requset):
        user_id = requset.query_params.get("id")
        previouse_date = requset.query_params.get("previous_date")
        
        service = MemoDomainService.initialize()
        
        if previouse_date:
            memos = service.get_memos_by_user_and_date(user_id, previous_date=previouse_date)
        else:
            memos = service.get_memos_by_user(user_id)

class GetMemoListByFollowingUsersAPIView(APIView):
    """自分自身のフォローしている人たちのメモを取得するAPI。"""
    def get(self, request):
        user = request.user
        previous_date = request.query_params.get("previous_date")
        
        service = MemoDomainService.initialize()
        
        if previous_date:
            memos = service.get_memos_by_following_users_and_me_and_date(user, previous_date)
        else:
            memos = service.get_memos_by_following_users(user)
        
        serializer = ReadingMemoSerializer(memos, many=True)
        return Response(serializer.data)
        


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


@login_required
def create_memo_api(request, book_id):
    if request.method == "POST":
        usecase = CreateMemoUsecase.build()

        response_data = usecase.run(request.POST, request.user, book_id)

        if response_data["result"] == "success":
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse(response_data, status=400)
    else:
        return JsonResponse({"result": "fail"}, status=400)


@login_required
def memo_delete_api(request, memo_id):
    if request.method == "DELETE":
        usecase = DeleteMemoUsecase(memo_id, request.user, ReadingMemoRepository())
        response_data = usecase.execute()

        if response_data["result"] == "success":
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse(response_data, status=400)
