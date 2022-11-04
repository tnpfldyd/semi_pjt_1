from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    celsius = models.FloatField(default=36.5)
    blocking = models.ManyToManyField('self', symmetrical=False, related_name='blockers')

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    introduce = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to="profile/", blank=True)
