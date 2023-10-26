from rest_framework.serializers import ModelSerializer

from authentication.models import Account

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password', 'profile_image',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': { 'write_only': True }
        }

    def create(self, validated_data):
        account = Account(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        account.set_password(validated_data['password'])
        account.save()
        return account