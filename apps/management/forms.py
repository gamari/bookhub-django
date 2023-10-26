from django import forms

from apps.management.models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', "kind")