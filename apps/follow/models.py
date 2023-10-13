from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(
        verbose_name="フォローしているユーザー",
        to=User, 
        on_delete=models.CASCADE, 
        related_name="following"
    )
    followed = models.ForeignKey(
        verbose_name="フォローされてる側",
        to=User, 
        on_delete=models.CASCADE, 
        related_name="followers"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")
    
