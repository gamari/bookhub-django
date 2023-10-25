from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView

from apps.book.application.usecases import (
    AddBookToShelfUsecase,
    RemoveBookFromShelfUsecase,
)


class ToggleBookOnShelfApiView(APIView):
    def post(self, request, book_id):
        usecase = AddBookToShelfUsecase.build()
        usecase.execute(book_id, request.user)
        return JsonResponse({"message": "追加に成功しました。"}, status=200)

    def delete(self, request, book_id):
        usecase = RemoveBookFromShelfUsecase.build()
        usecase.execute(book_id, request.user)
        return JsonResponse({"message": "削除に成功しました。"}, status=200)


