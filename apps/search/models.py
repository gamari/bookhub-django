from django.db import models
from django.contrib.auth import get_user_model

Account = get_user_model()

class SearchHistory(models.Model):
    query = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)