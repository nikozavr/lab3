from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from session.models import Users
import json
import hashlib
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
import logging
from django.conf import settings

# Create your views here.
@csrf_exempt
def create(request):
	if request.method == "POST":
		data = request.body
		data = json.loads(data.decode('utf8'))
		login = data["login"]
		password = data["password"]
		logger = logging.getLogger('lab3')
		try:
			user = Users.objects.get(login=login)
			if user.password == password: #check_password(password, user.password):
				session_key = ""
				if cache.get(session_key) != None:	
					cache.delete(session_key)
				session_key = create_session(user)
				cache.set(session_key, user.id)	
				json_data = json.dumps({"user_id": user.id, "session_key": session_key})
				logger.info(json_data)
				return HttpResponse(json_data, content_type="application/json")
			else: 
				with open(settings.STATIC_ROOT + '/jsons/error_log_pas.json') as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=400)
		except ObjectDoesNotExist:
			with open(settings.STATIC_ROOT + '/jsons/error_log_pas.json') as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=400)

	return HttpResponse("Ok")
			#return  json.loads(open('/static/jsons/error_log_pas.json').read()), 0

@csrf_exempt
def check(request):
	if request.method == "POST":
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		user_id = int(session_key[:3])
		s = cache.get(session_key)
		if s == user_id:
			try:
				user = Users.objects.get(pk=user_id)
				with open(settings.STATIC_ROOT + '/jsons/check_ok.json') as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data))
			except ObjectDoesNotExist:
				with open(settings.STATIC_ROOT + '/jsons/error_check.json') as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=400)
		else:
			with open(settings.STATIC_ROOT + '/jsons/error_check.json') as data_file:    
					data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=400)

@csrf_exempt
def refresh(request):
	if request.method == "POST":
		return HttpResponse("Ok")


def create_session(user):
	now = datetime.utcnow().replace(tzinfo=utc)
	session_key = hashlib.sha224(user.login.encode('utf-8') + user.password.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
	while cache.get(session_key) != None:
		session_key = hashlib.sha224(user.login.encode('utf-8') + user.password.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
	session_key = ("%03d" % user.id) + session_key
	return session_key


@csrf_exempt
def userinfo(request):
	if request.method == "POST":
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		user_id = int(session_key[:3])

		logger = logging.getLogger('lab3')

		logger.info(session_key)
		logger.info(user_id)
		s = cache.get(session_key)
		logger.info(s)
		if s == user_id:
			try:
				user = Users.objects.get(pk=user_id)
				data = json.dumps(user.as_json())
				logger.info(data)
				return HttpResponse(data)
			except ObjectDoesNotExist:
				with open(settings.STATIC_ROOT + '/jsons/error_check.json') as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=400)
		else:
			with open(settings.STATIC_ROOT + '/jsons/error_check.json') as data_file:    
					data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=400)