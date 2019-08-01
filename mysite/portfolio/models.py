from django.db import models
from django.contrib.auth.models import User

class Stocks(models.Model):
    ticker = models.TextField(primary_key=True, unique=True, blank=False, null=False)
    name = models.TextField(blank=True, null=True)
    momentum = models.FloatField(blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stocks'
        verbose_name_plural = "stocks"
