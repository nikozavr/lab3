from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from session import Users
import json

# Create your views here.
def index(request):
	if request.method == "POST":
		login = request.POST.get("login")
		password = request.POST.get("password")
		try:
			user = Users.objects.get(login=login)
			if check_password(password, user.password):

			else: 
				return json.load(json.open("/static/jsons/error_log_pas.json"))
		except ObjectDoesNotExist:
			return json.load(json.open("/static/jsons/error_log_pas.json"))
	
	return HttpResponse("OK")