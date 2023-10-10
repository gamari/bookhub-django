from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
