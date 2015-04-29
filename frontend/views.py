from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import requests
import json
from django.core.cache import cache

# Create your views here.
def home(request):
	return HttpResponse("OK")

@csrf_exempt
def index(request):
	post_data = {"login":"nikozavr",
				"password":"nikitos1"}

	headers = {'Content-type': 'application/json'}	
	logger = logging.getLogger('lab3')		
	s = cache.get(1234)

	try:
		if request.session['session_key'] != None:
			return render(request, 'frontend/index.html', )	
	except KeyError:
			return render(request, 'frontend/authorize.html', )	


	r = requests.post("http://localhost:8000/session/create/", data=json.dumps(post_data), headers=headers) 
	#return HttpResponse("Bad")
#	if correct == 1:
	
	return HttpResponse(r)
#	else:
#		return HttpResponse("Bad")

def check_user(request):
	post_data = {""}
	return HttpResponse("Ok")

def requests_manager(request):
	return HttpResponse("OK")

def register(request):
	return HttpResponse("OK")

def login(request):
	if request.method == "POST":
		error_text = ""
		login = request.POST.get("login", "")
		password = request.POST.get("password", "")
		post_data = {"login":login,
				"password":password}

		headers = {'Content-type': 'application/json'}	

		r = requests.post("http://localhost:8000/session/create/", data=json.dumps(post_data), headers=headers) 

		if r.status_code == requests.codes.ok:
			#data = request.body
			data = r.json()
		#	data = json.loads(data.decode('utf8'))
			logger = logging.getLogger('lab3')
			logger.info(data)
			logger.info(data["session_key"])
		#	data = json.loads(data.decode('utf8'))
			request.session['session_key'] = data["session_key"]
			return redirect("http://localhost:8000/")
		else:
			error_text = "Password is incorrect"
			return render(request, 'frontend/authorize.html', {"error_text": error_text})

def logout(request):
	try:
		del request.session['id']
	except KeyError:
		pass
	return redirect("http://localhost:8000/")