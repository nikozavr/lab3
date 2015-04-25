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


class Apps(models.Model):
    user = models.ForeignKey(Users)
    client_id = models.CharField(max_length=100, unique=True)
    client_secret = models.CharField(max_length=100, unique=True)

    @classmethod
    def create(cls, user):
        client_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        client_secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        app = user.apps_set.create(client_id=client_id, client_secret=client_secret)
        return app

class Token(models.Model):
	app_id = models.OneToOneField(Apps)
	access_token = models.CharField(max_length=100, null=True)
	token_type = models.CharField(max_length=50, null=True)
	refresh_token = models.CharField(max_length=100,null=True)
	token_expires = models.DateTimeField(null=True)
	redirect_uri = models.CharField(max_length=100, null=True)

	@classmethod
	def create(cls, app, redirect_uri = None):
		now = datetime.utcnow().replace(tzinfo=utc)
		string = app.client_id
		token = cls(app_id=app, redirect_uri=redirect_uri)
		token.token_type = "Bearer"
		now = datetime.utcnow().replace(tzinfo=utc)
		token.token_expires = now + timedelta(minutes = 4)
		token.access_token = hashlib.sha224('access'.encode('utf-8') + self.code.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		token.refresh_token = hashlib.sha224('refresh'.encode('utf-8') + self.code.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		return (self.access_token, self.refresh_token, self.token_expires.strftime(settings.DATE_FORMAT), self.token_type)

		def token_expired(self):
		return (self.token_expires - datetime.utcnow().replace(tzinfo=utc) > timedelta(seconds=0))

	def create_token(self):
		self.token_type = "Bearer"
		now = datetime.utcnow().replace(tzinfo=utc)
		self.token_expires = now + timedelta(minutes = 4)
		self.access_token = hashlib.sha224('access'.encode('utf-8') + self.code.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		self.refresh_token = hashlib.sha224('refresh'.encode('utf-8') + self.code.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
		return (self.access_token, self.refresh_token, self.token_expires.strftime(settings.DATE_FORMAT), self.token_type)

class CurrentUser(models.Model):
	user = models.ForeignKey(Users)