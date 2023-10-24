from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    kind = models.CharField(max_length=100, default="news")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title