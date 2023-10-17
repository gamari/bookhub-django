from django import forms

from apps.book.models import Book, BookSelection, Bookshelf

class BookSelectionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'value': '',
                'placeholder': 'セレクション名',
            }
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'セレクションの説明を書いて下さい……',
                'rows': 5,
            }
        ),
    )

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
    
    def clean_books(self):
        books = self.cleaned_data['books']
        if len(books) < 1:
            raise forms.ValidationError('書籍は1冊以上選択してください。')
        if len(books) >= 100:
            raise forms.ValidationError('書籍は100冊以下選択してください。')
        return books
