
from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    login = models.CharField('Имя пользователя', unique=True, db_index=True, max_length=100)
    password = models.CharField('Пароль', max_length=100)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'login'

    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['login']
        db_table = "users"
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
