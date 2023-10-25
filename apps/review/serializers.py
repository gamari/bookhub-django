from rest_framework import serializers

from apps.review.models import ReviewLike


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'
        read_only_fields = ('review', 'user')