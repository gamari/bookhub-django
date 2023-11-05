from django import forms
from apps.note.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'is_public']
        widgets = {
            "content": forms.Textarea(attrs={"rows": 20, "cols": 80, "id": "note-content"}),
        }