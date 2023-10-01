from django import forms
from .models import Account

class AccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['username'].widget.attrs.update({'class': 'form-input'})
        self.fields['profile_image'].widget.attrs.update({'class': 'form-input-file'})

    class Meta:
        model = Account
        fields = ['email', 'username', 'description', 'profile_image']
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 1:
            raise forms.ValidationError("1文字以上を入力してください")
        return username
