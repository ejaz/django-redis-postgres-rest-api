from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=70, blank=False, default='')
    # price = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)