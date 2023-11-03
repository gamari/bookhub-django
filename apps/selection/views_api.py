import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.selection.application.usecases import AICreateSelectionUsecaseByDemand
from apps.selection.serializers import BookSelectionSerializer
from config.exceptions import ApplicationException

from .models import BookSelection, BookSelectionLike

logger = logging.getLogger("app_logger")

Account = get_user_model()


class SelectionDetailAPIView(APIView):
    def delete(self, request, selection_id):
        logger.debug(f"id={selection_id}を削除します")
        selection = get_object_or_404(BookSelection, id=selection_id)

        if selection.user.id != request.user.id:
            return Response({"detail": "他のユーザーのセレクションは削除できません。"}, status=status.HTTP_400_BAD_REQUEST)

        selection.delete()
        return Response({"detail": "セレクションを削除しました。"}, status=status.HTTP_200_OK)


class LikeBookSelectionApiView(APIView):
    """いいね機能API"""
    
    def post(self, request, selection_id):
        user = request.user
        selection = get_object_or_404(BookSelection, id=selection_id)

        existing_like = BookSelectionLike.objects.filter(user=user, selection=selection).first()

        if existing_like:
            existing_like.delete()
            action = "unliked"
        else:
            BookSelectionLike.objects.create(user=user, selection=selection)
            action = "liked"

        return Response({'action': action})


class AICreateSelectionAPIView(APIView):
    def post(self, request):
        demand = request.data.get("demand")

        if not request.user.is_staff and request.user.is_available_ai():
            return Response({"detail": "利用可能なセレクション数を超えています。"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 楽観的ロック
        current_value = Account.objects.get(id=request.user.id).available_selections
        if current_value != request.user.available_selections:
            return Response({"detail": "同時に複数のリクエストが処理されています。再試行してください。"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usecase = AICreateSelectionUsecaseByDemand.build()
            selection = usecase.run(demand, request.user)
            serializer = BookSelectionSerializer(selection)

            request.user.available_ai -= 1
            request.user.save()

            return Response(serializer.data, status=201)
        except ApplicationException as e:
            return Response({"detail": "作成できませんでした。"}, status=status.HTTP_400_BAD_REQUEST)
