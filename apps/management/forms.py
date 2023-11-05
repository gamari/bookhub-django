from django import forms

from apps.management.models import Notice, Tweet, TweetTag

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', "kind")

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ('content', "is_active")
        
class TweetTagForm(forms.ModelForm):
    class Meta:
        model = TweetTag
        fields = ('title',)