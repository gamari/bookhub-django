from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import BookSelection, BookSelectionLike


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

