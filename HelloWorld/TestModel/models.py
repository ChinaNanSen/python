from asyncio.windows_events import NULL
from django.db import models

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=20,null=False)
    age = models.IntegerField(max_length=100,default=0)
    sex = models.CharField(max_length=10,null=False)
    bank = models.CharField(max_length=10,null=False)