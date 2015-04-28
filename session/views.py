from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from session import Users
import json
import hashlib
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.core.cashe import cache

# Create your views here.
def index(request):
	if request.method == "POST":
		data = json.loads(request.body)
		login = data["login"]
		password = data["password"]
		return HttpResponse("Ok")
		try:
			user = Users.objects.get(login=login)
			if check_password(password, user.password):
				now = datetime.utcnow().replace(tzinfo=utc)
				session_key = hashlib.sha224(user.login.encode('utf-8') + user.password.encode('utf-8') + now.strftime(settings.DATE_FORMAT).encode('utf-8')).hexdigest()
				#cache.set(user.id, session_key)
				return JsonResponse(json.dumps({"user_id": user.id, "session_key", session_key}))
			else: 
				return HttpResponse("Ok")
				#return json.loads(open('/static/jsons/error_log_pas.json').read()), 0
		except ObjectDoesNotExist:
			return HttpResponse("Ok")
			#return  json.loads(open('/static/jsons/error_log_pas.json').read()), 0
