from django import forms
from django.forms import ValidationError

from apps.record.models import ReadingMemo


class ReadingMemoForm(forms.ModelForm):
    class Meta:
        model = ReadingMemo
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'memo-textarea', 
                'placeholder': '感想やページ数をメモ……(500文字以内)',
                "maxLength": "500"
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > 500:
            raise ValidationError("1000文字以内で入力してください。")
        return content