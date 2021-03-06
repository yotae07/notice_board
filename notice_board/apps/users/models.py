from django.contrib.auth import models as auth_models
from django.contrib.auth.models import UserManager as AuthUserManager
from django.db import models

from ..models import BaseModel


class CustomUserManager(AuthUserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)


class User(auth_models.AbstractBaseUser, BaseModel):
    ADMIN, GENERAL, MANAGER = ('admin', 'general', 'manager')
    USER_TYPE_CHOICES = (
        (ADMIN, 'admin'),
        (GENERAL, 'general'),
        (MANAGER, 'manager')
    )

    username = models.CharField(verbose_name='id', max_length=32, unique=True)
    name = models.CharField(verbose_name='name', max_length=30)
    role = models.CharField(verbose_name='authority', max_length=10, default=GENERAL, choices=USER_TYPE_CHOICES)
    phone = models.CharField(verbose_name='phone', max_length=20, db_index=True)
    email = models.EmailField(verbose_name='email', max_length=100, db_index=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return f"{self.username} {self.name} {self.role}"

    @property
    def join_at(self):
        return f'{self.created_at:%Y-%m-%d} 00:00:00.000Z'

    @property
    def is_staff(self):
        return True

    @property
    def is_superuser(self):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
