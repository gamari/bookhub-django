import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です。")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=256, unique=True, null=False, blank=False)
    username = models.CharField(max_length=30, unique=True, default="noname")
    description = models.TextField(max_length=500, blank=True, null=True)
    is_ai = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    available_selections = models.IntegerField(verbose_name="セレクション作成の有効数。",default=3)
    available_ai = models.IntegerField(verbose_name="AIの利用可能数。",default=3)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects: AccountManager = AccountManager()
    
    def __str__(self) -> str:
        return f"[{self.username}] {self.email}"

    def is_following(self, target_user) -> bool:
        """自分がtarget_userをフォローしているかどうかを返す"""
        from apps.follow.models import Follow

        return Follow.objects.filter(follower=self, followed=target_user).exists()
    
    def bookshelf(self):
        from apps.book.models import Bookshelf
        return Bookshelf.objects.get(user=self)
    
    # AIの利用可能判定
    def is_available_ai(self):
        return self.available_ai > 0
