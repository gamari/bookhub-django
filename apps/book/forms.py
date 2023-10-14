from django import forms

from apps.book.models import Book, BookSelection, Bookshelf


# class BookSelectionForm(forms.ModelForm):
#     class Meta:
#         model = BookSelection
#         fields = ['title', 'books', 'description']

class BookSelectionForm(forms.ModelForm):
    class Meta:
        model = BookSelection
        fields = ['title', 'books', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BookSelectionForm, self).__init__(*args, **kwargs)

        if user:
            try:
                bookshelf = Bookshelf.objects.get(user=user)
                self.fields['books'].queryset = bookshelf.books.all()
            except Bookshelf.DoesNotExist:
                self.fields['books'].queryset = Book.objects.none()