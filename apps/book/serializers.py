from rest_framework.serializers import ModelSerializer

from apps.book.models import Book

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        