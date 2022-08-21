from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Users(AbstractUser):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    username = models.CharField(max_length=150, unique=True, db_index=True, help_text="用户账号", verbose_name="用户账号")
    avatar = models.CharField(max_length=255, null=True, help_text="头像", verbose_name="头像")

    class Meta:
        db_table = "users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
