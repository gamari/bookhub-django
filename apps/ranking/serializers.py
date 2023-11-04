from rest_framework import serializers

from authentication.models import Account

class UserMemosRankSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'username', "profile_image", 'rank', 'count') 