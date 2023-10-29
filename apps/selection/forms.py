from apps.book.models import Book, Bookshelf
from apps.selection.models import BookSelection


from django import forms


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
    is_public = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[
            (True, '公開'),
            (False, '非公開'),
        ],
        initial=False,
    )

    class Meta:
        model = BookSelection
        fields = ['title', 'books', 'description', 'is_public']

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