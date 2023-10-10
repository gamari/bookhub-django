from django import forms
from record.models import ReadingMemo


class ReadingMemoForm(forms.ModelForm):
    class Meta:
        model = ReadingMemo
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'memo-textarea', 'placeholder': '感想やページ数をメモ……'}),
        }
