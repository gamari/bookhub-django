from django.db import models


class Contact(models.Model):
    CONTACT_CHOICES = (
        ("error", "エラー・バグ報告"),
        ("book", "書籍問い合わせ"),
        ("other", "その他"),
    )

    contact_type = models.CharField(max_length=10, choices=CONTACT_CHOICES)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)
    memo = models.TextField(blank=True, null=True, verbose_name="備考欄")
