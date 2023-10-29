from django import forms

from apps.book.models import Book

class DateInput(forms.DateInput):
    input_type = 'date'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'id', 
            'isbn_10', 'isbn_13', 'other', 
            'title', 'description', 
            'category', 
            'thumbnail', 
            'published_date', 
            'publisher', 
            'views', 
            'is_clean'
        ]
        widgets = {
            'published_date': DateInput(),
        }


