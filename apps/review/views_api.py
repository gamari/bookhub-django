import logging

from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError

from .models import  ReviewLike
from .serializers import ReviewLikeSerializer


logger = logging.getLogger("app_logger")

class ReviewLikeAPIView(generics.CreateAPIView):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get('pk') 
        user = self.request.user

        is_liked = ReviewLike.objects.filter(user=user, review__id=review_id).exists()
        if is_liked:
            raise ValidationError({"detail": "既にいいねしています。"})
        
        serializer.save(user=user, review_id=review_id)

class ReviewUnLikeAPIView(generics.DestroyAPIView):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    lookup_field = 'pk'

    def get_object(self):
        user = self.request.user
        review_id = self.kwargs.get(self.lookup_field)
        
        try:
            return ReviewLike.objects.get(user=user, review__id=review_id)
        except ReviewLike.DoesNotExist:
            raise NotFound(detail="いいねの解除ができません。")

    def perform_destroy(self, instance):
        instance.delete()