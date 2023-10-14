from django import forms

from apps.book.models import Book, BookSelection


class BookSelectionForm(forms.ModelForm):
    class Meta:
        model = BookSelection
        fields = ['books', 'description']