import logging

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.selection.application.usecases import AICreateSelectionUsecase
from apps.selection.serializers import BookSelectionSerializer

from .models import BookSelection, BookSelectionLike

logger = logging.getLogger("app_logger")

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
        usecase = AICreateSelectionUsecase.build()
        selection = usecase.run(demand, request.user)
        serializer = BookSelectionSerializer(selection)
        return Response(serializer.data, status=201)
