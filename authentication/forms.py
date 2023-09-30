from django import forms
from .models import Account

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise forms.ValidationError("5文字以上で入力してください")
        return username
