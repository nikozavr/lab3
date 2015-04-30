from django.db import models

from backend_manufacturers.models import Manufacturers

# Create your models here.
class Devices(models.Model):
	manufacturer = models.ForeignKey(Manufacturers)
	name = models.CharField(max_length=100)
	device_type = models.CharField(max_length=50)
	dig_disp = models.FloatField()
	year = models.IntegerField()

	def as_json(self):
		return dict(id=self.id, manufacturer=self.manufacturer.name,
			name=self.name, 
			device_type=self.device_type,
			dig_disp=self.dig_disp,
			year=self.year)