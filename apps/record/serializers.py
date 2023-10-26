from rest_framework import serializers

from apps.record.models import ReadingMemo

class ReadingMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingMemo
        fields = '__all__'