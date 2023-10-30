from rest_framework.serializers import ModelSerializer

from apps.selection.models import BookSelection

class BookSelectionSerializer(ModelSerializer):
    class Meta:
        model = BookSelection
        fields = '__all__'