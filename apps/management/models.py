from django.db import models
import markdown

class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    content_html = models.TextField(default="", blank=True, null=True)
    kind = models.CharField(max_length=100, default="news")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.content_html = markdown.markdown(self.content)
        super().save(*args, **kwargs)

class Tweet(models.Model):
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
