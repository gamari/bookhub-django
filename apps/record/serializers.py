from rest_framework import serializers
from apps.book.serializers import BookSerializer

from apps.record.models import ReadingMemo
from authentication.serializers import AccountSerializer


class ReadingMemoSerializer(serializers.ModelSerializer):
    user = AccountSerializer()
    book = BookSerializer()

    class Meta:
        model = ReadingMemo
        fields = '__all__'