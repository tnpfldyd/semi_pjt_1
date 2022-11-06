
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
# Create your models here.

class Products(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    # ImageSpecField : 원본 ImageField로부터 생성(원본o, 썸네일o)
    original_image = models.ImageField(upload_to='photos')
    formatted_image = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(200,200)],
        format='JPEG',
        options={'quality':100}
    )
    price = models.IntegerField()
    hit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zzim = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='zzim_pro')
    sold = models.BooleanField(default=False)
    
class Location(models.Model):
    trade_locationx = models.CharField(max_length=100)
    trade_locationy = models.CharField(max_length=100)
    product = models.OneToOneField(Products, on_delete=models.CASCADE)

class Popularsearch(models.Model):
    terms = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    searchCount = models.IntegerField(default=1)