from django import forms
from record.models import ReadingMemo


class ReadingMemoForm(forms.ModelForm):
    class Meta:
        model = ReadingMemo
        fields = ['content']
