from django.db import models
from django.contrib.auth.models import AbstractUser
# from model_utils.models import TimeStampedModel

# Create your models here.
class User(AbstractUser):
    phone = models.TextField(max_length=11, blank=False)
    is_verified = models.BooleanField(default=False)

class AuthSmsSignIn(models.Model):
    phone_number = models.TextField(max_length=11, blank=False)
    auth_number = models.IntegerField(verbose_name="인증 번호")

