import logging
from django import forms
from django.core.exceptions import ValidationError

from .models import Review

logger = logging.getLogger("app_logger")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]
        labels = {"rating": "評価", "content": "レビュー内容"}
        widgets = {
            "rating": forms.Select(attrs={
                "class": "form-select"
            }),
            "content": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-textarea",
                    "placeholder": "感想を記入……(2000)",
                }
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None:
            raise ValidationError("レーティングは必須です。")
        return rating
