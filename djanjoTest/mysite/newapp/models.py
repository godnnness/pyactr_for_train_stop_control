from django.db import models

# Create your models here.
class Zhuce(models.Model):
    user=models.CharField(max_length=20)
    pwd=models.CharField(max_length=32)
    ss=models.CharField(max_length=32)

