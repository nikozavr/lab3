from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging
import requests
from backend_devices.models import Devices, Manufacturers
import json
import os

@csrf_exempt
def list(request):
	if request.method == "GET":
		devices = Devices.objects.all()
		results = [ob.as_json() for ob in devices]
		result = {"count": Devices.objects.count(), "devices": results}
		return HttpResponse(json.dumps(result))
	return HttpResponse("Ok")

@csrf_exempt
def remove(request):
	if request.method == "POST":
		logger = logging.getLogger('backend_device')
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		device_id = data["device_id"]
		post_data = {"session_key": session_key}
		headers = {'Content-type': 'application/json'}	
		check = requests.post("http://localhost:8000/session/check/", data=json.dumps(post_data), headers=headers)
		logger.info(check)
		if check.status_code == requests.codes.ok:
			try:
				device = Devices.objects.get(pk=device_id)
				device.delete()
				return HttpResponse(json.dumps({"info":"Success deleting"}))
			except ObjectDoesNotExist:
				with open(os.path.join(settings.BASE_DIR, "static/jsons/device_not_found.json")) as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=404)
		else:
			logger.info("delete")
			with open(os.path.join(settings.BASE_DIR, "static/jsons/error_check.json")) as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=401)

@csrf_exempt
def add(request):
	if request.method == "POST":
		logger = logging.getLogger('backend_manufacturer')
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		manufacturer_id = data["manufacturer_id"]
		device_type = data["device_type"]
		dig_disp = data["dig_disp"]
		year = data["year"]
		name = data["name"]
		post_data = {"session_key": session_key}
		headers = {'Content-type': 'application/json'}	
		check = requests.post("http://localhost:8000/session/check/", data=json.dumps(post_data), headers=headers)
		if check.status_code == requests.codes.ok:
			try:
				logger.info("data")
				manufacturer = Manufacturers.objects.get(pk=int(manufacturer_id))
				logger.info("data")
				device = manufacturer.devices_set.create(name=name,device_type=device_type,dig_disp=float(dig_disp),year=int(year))
				logger.info("data")
				data = json.dumps({"info":"Success adding"})
				logger.info(data)
				return HttpResponse(data)
			except ObjectDoesNotExist:
				with open(os.path.join(settings.BASE_DIR, "static/jsons/manufacturer_not_found.json")) as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=404)
		else:
			with open(os.path.join(settings.BASE_DIR, "static/jsons/error_check.json")) as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=401)
		
	return HttpResponse("Ok")