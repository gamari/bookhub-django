from django import forms
from django.core.exceptions import ValidationError

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]
        labels = {"rating": "評価", "content": "レビュー内容"}
        widgets = {
            "rating": forms.Select(attrs={
                "class": "form-select",
                "value": 5
            }),
            "content": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-textarea",
                    "placeholder": "感想を記入……",
                }
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 0:
            raise ValidationError("内容は0文字以上でなければなりません。")
        return content

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None:
            raise ValidationError("レーティングは必須です。")
        return rating
