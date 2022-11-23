from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField
from . import managers
import jwt
from datetime import datetime, timedelta
from django.conf import settings
# Create your models here.


class TimestampedModel(models.Model):

    # 생성된 날짜를 기록
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정된 날짜를 기록
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = [
        'nickname',
        'password'
    ]
    objects = managers.UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        return token
