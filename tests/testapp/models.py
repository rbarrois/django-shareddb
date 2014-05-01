from django.db import models

# Create your models here.

class Something(models.Model):
    data = models.CharField(max_length=10)
