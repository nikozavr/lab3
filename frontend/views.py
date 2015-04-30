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
#	post_data = {"login":"nikozavr",
#				"password":"nikitos1"}

#	headers = {'Content-type': 'application/json'}	
	logger = logging.getLogger('lab3')		


	r_manufacturers = requests.get("http://localhost:8000/backend_manufacturers/list/")
	try:
		data_manufacturers = r_manufacturers.json()
	except ValueError:
		data_manufacturers = {"count": 0}

	r_devices = requests.get("http://localhost:8000/backend_devices/list/")	
	
	try:
		data_devices = r_devices.json()	
	except ValueError:
		data_devices = {"count": 0}
	logger.info("Oppp")
	if 'session_key' in request.session:
		post_data = {"session_key":request.session['session_key']}
		headers = {'Content-type': 'application/json'}
		logger.info("Oppp")
		r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
		logger.info("Oppp")
		logger.info(r_user)
		if r_user.status_code == requests.codes.ok:
			data_user = r_user.json()
			logger.info(data_user)
			logger.info(data_manufacturers)
			context = { "data_manufacturers": data_manufacturers,
						"data_devices": data_devices,
						"data_user": data_user								
						}
		else:
			context = { "data_manufacturers": data_manufacturers,
						"data_devices": data_devices,
						"data_user": 0							
						}
		return render(request, 'frontend/index.html', context)
	

	else:
		context = { "data_manufacturers": data_manufacturers,
						"data_devices": data_devices,
						"data_user": 0							
						}
		return render(request, 'frontend/index.html', context)

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
			data = r.json()
			logger = logging.getLogger('lab3')
			logger.info(data)
			request.session['session_key'] = data["session_key"]
			return redirect("http://localhost:8000/")
		else:
			error_text = "Password is incorrect"
			return render(request, 'frontend/authorize.html', {"error_text": error_text})
	if request.method == "GET":
		return render(request, 'frontend/authorize.html', )	
	return HttpResponse("Ok")

def logout(request):
	try:
		del request.session['session_key']
	except KeyError:
		pass
	return redirect("http://localhost:8000/")


def del_device(request, device_id):
	if request.method == "GET":
		if 'session_key' in request.session:
			post_data = {"session_key":request.session['session_key'], "device_id": device_id}
			headers = {'Content-type': 'application/json'}
			result = requests.post("http://localhost:8000/backend_devices/remove/", data=json.dumps(post_data), headers=headers) 




	return HttpResponse("Ok")


def del_manufacturer(request, manufacturer_id):
	if request.method == "GET":
		if 'session_key' in request.session:
			post_data = {"session_key":request.session['session_key'], "manufacturer_id": device_id}
			headers = {'Content-type': 'application/json'}
			result = requests.post("http://localhost:8000/backend_manufacturers/remove/", data=json.dumps(post_data), headers=headers) 

	return HttpResponse("Ok")


def edit_device(request, device_id):

	return HttpResponse("Ok")


def edit_manufacturer(request, manufacturer_id):

	return HttpResponse("Ok")