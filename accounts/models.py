from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.core.validators import RegexValidator

REGEX = '^[a-zA-Z0-9.+-]*$'


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)

AUTH_PROVIDERS = {'email': 'email',}

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField('آدرس ایمیل', unique=True, null=True)
    username = models.CharField('نام کاربری', max_length=30, unique=True, validators=[RegexValidator(
        regex=REGEX, message="username must contain alphabets and numbers only", code='invalid username')])
    first_name = models.CharField('نام', max_length=254, null=True)
    last_name = models.CharField('نام خانوادگی', max_length=254, null=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('تاریخ عضویت', default=timezone.now)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر ها'
