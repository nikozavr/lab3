from django.db import models

# Create your models here.
class Manufacturers(models.Model):
	name = models.CharField(max_length=30)
	established = models.IntegerField()
	country = models.CharField(max_length=30)