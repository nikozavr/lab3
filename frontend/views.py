from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import requests
import json
from django.core.cache import cache
from django.contrib import messages

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
	if 'session_key' in request.session:
		post_data = {"session_key":request.session['session_key']}
		headers = {'Content-type': 'application/json'}
		logger.info(post_data)
		r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
		if r_user.status_code == requests.codes.ok:
			data_user = r_user.json()
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
		logger = logging.getLogger('lab3')
		if 'session_key' in request.session:
			post_data = {"session_key":request.session['session_key'], "device_id": device_id}
			headers = {'Content-type': 'application/json'}
			logger.info(post_data)
			result = requests.post("http://localhost:8000/backend_devices/remove/", data=json.dumps(post_data), headers=headers) 
			if result.status_code == requests.codes.ok:
				return redirect("http://localhost:8000/")
			else:
				messages.add_message(request, messages.INFO, 'Hello world.')


	return HttpResponse("Ok")


def del_manufacturer(request, manufacturer_id):
	if request.method == "GET":
		logger = logging.getLogger('lab3')
		if 'session_key' in request.session:
			post_data = {"session_key":request.session['session_key'], "manufacturer_id": manufacturer_id}
			headers = {'Content-type': 'application/json'}
			logger.info(post_data)
			result = requests.post("http://localhost:8000/backend_manufacturers/remove/", data=json.dumps(post_data), headers=headers) 
			if result.status_code == requests.codes.ok:
				return redirect("http://localhost:8000/")
			else:
				messages.add_message(request, messages.ERROR, 'Error delete')

	return HttpResponse("Ok")


def edit_device(request, device_id):

	return HttpResponse("Ok")


def edit_manufacturer(request, manufacturer_id):

	return HttpResponse("Ok")

def add_device(request):
	if request.method == "GET":
		if 'session_key' in request.session:
			logger = logging.getLogger('lab3')
			post_data = {"session_key":request.session['session_key']}
			headers = {'Content-type': 'application/json'}
			logger.info(post_data)
			r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
			r_manufacturers = requests.get("http://localhost:8000/backend_manufacturers/list/")
			try:
				data_manufacturers = r_manufacturers.json()
			except ValueError:
				data_manufacturers = {"count": 0}
			if r_user.status_code == requests.codes.ok:
				data_user = r_user.json()
				context = {"data_user": data_user,
							"data_manufacturers": data_manufacturers
							}
			else:
				context = {	"data_user": 0,
							"data_manufacturers": data_manufacturers
							}
			return render(request, "frontend/add_device.html", context)
	if request.method == "POST":
		if 'session_key' in request.session:
			logger = logging.getLogger('lab3')
			name = request.POST.get("name","")
			manufacturer_id = request.POST.get("manufacturer_id","")
			device_type = request.POST.get("device_type","")
			dig_disp = request.POST.get("dig_disp","")
			year = request.POST.get("year","")
			post_data = {"session_key":request.session['session_key'], "name": name, "manufacturer_id":manufacturer_id, "device_type": device_type, "dig_disp":dig_disp, "year": year}
			headers = {'Content-type': 'application/json'}
			logger.info(post_data)
			result = requests.post("http://localhost:8000/backend_devices/add/", data=json.dumps(post_data), headers=headers) 
			if result.status_code == requests.codes.ok:
				return redirect("http://localhost:8000/")
			else:
				messages.add_message(request, messages.INFO, 'Error add.')


def add_manufacturer(request):
	if request.method == "GET":
		if 'session_key' in request.session:
			logger = logging.getLogger('lab3')
			post_data = {"session_key":request.session['session_key']}
			headers = {'Content-type': 'application/json'}
			logger.info(post_data)
			r_user = requests.post("http://localhost:8000/session/userinfo/", data=json.dumps(post_data), headers=headers) 
			if r_user.status_code == requests.codes.ok:
				data_user = r_user.json()
				context = {"data_user": data_user								
							}
			else:
				context = {	"data_user": 0							
							}
			return render(request, "frontend/add_manufacturer.html", context)
	if request.method == "POST":
		if 'session_key' in request.session:
			logger = logging.getLogger('lab3')
			name = request.POST.get("name","")
			established = request.POST.get("established","")
			country = request.POST.get("country","")
			post_data = {"session_key":request.session['session_key'], "name": name, "established":established, "country": country}
			headers = {'Content-type': 'application/json'}
			logger.info(post_data)
			result = requests.post("http://localhost:8000/backend_manufacturers/add/", data=json.dumps(post_data), headers=headers) 
			if result.status_code == requests.codes.ok:
				return redirect("http://localhost:8000/")
			else:
				messages.add_message(request, messages.INFO, 'Error add.')