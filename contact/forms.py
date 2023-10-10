from django import forms
from django import forms

from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["contact_type", "email", "content"]
        widgets = {
            "contact_type": forms.Select(attrs={"class": "max-w-sm"}),
            "email": forms.EmailInput(attrs={"class": "max-w-md"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
