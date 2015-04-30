from django.db import models
from django.core.signing import Signer
from django.contrib.auth.hashers import make_password

import string
import random
import hashlib
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.conf import settings

# Create your models here.
class Users(models.Model):
	login = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	name = models.CharField(max_length=30)
	phone = models.CharField(max_length=20)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.login;

	@classmethod
	def create(cls, login, email, name, phone, password):
		password = make_password(password, None, 'md5')
		user = cls(login=login, email=email, name=name, phone=phone, password=password)
		return user

	def as_json(self):
		return dict(login=self.login, email=self.email,
					name=self.name, phone=self.phone)
