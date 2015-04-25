from django.db import models

# Create your models here.
class Devices(models.Model):
	manufacturer = models.ForeignKey(Manufacturers)
	name = models.CharField(max_length=100)
	device_type = models.CharField(max_length=50)
	dig_disp = models.FloatField()
	year = models.IntegerField()