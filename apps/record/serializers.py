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
    
    def get_created_at_jp(self, obj):
        return obj.created_at.strftime('%Y/%m/%d')