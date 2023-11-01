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
            'is_clean',
            "amazon_url",
            "tags",
        ]
        widgets = {
            'published_date': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["tags"].queryset = self.instance.tags.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.views += 5
        if commit:
            instance.save()
            self.save_m2m()
        return instance

