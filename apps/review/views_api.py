import logging

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError

from apps.review.application.usecases import DeleteReviewUsecase, ReviewUsecase

from .models import  ReviewLike
from .serializers import ReviewLikeSerializer


logger = logging.getLogger("app_logger")

class ReviewDetailAPIView(APIView):
    @method_decorator(login_required)
    def post(self, request, book_id, *args, **kwargs):
        logger.debug(request.data)
        usecase = ReviewUsecase(request.user, book_id, request.data)

        usecase.execute()
        return Response({
            "message": "作成に成功しました"
        }, status=201)
    
    @method_decorator(login_required)
    def delete(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        logger.debug(book_id)

        usecase = DeleteReviewUsecase(request.user, book_id)
        usecase.execute()
        
        return Response({
            "message": "削除に成功しました"
        }, status=204)


class ReviewLikeAPIView(CreateAPIView):
    """ReviewいいねAPI。"""
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get('pk') 
        user = self.request.user

        is_liked = ReviewLike.objects.filter(user=user, review__id=review_id).exists()
        if is_liked:
            raise ValidationError({"detail": "既にいいねしています。"})
        
        serializer.save(user=user, review_id=review_id)

class ReviewUnLikeAPIView(DestroyAPIView):
    """Reviewいいね解除API。"""
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