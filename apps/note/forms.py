from django import forms
from apps.note.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'is_public']
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12, "id": "note-content", "class": "textarea w-full"}),
            "title": forms.TextInput(attrs={"id": "note-title", "class": "input"}),
        }