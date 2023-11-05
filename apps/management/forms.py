from django import forms

from apps.management.models import Notice, Tweet

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', "kind")

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('content',)