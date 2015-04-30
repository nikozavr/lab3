from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from backend_manufacturers.models import Manufacturers
import json
import requests

# Create your views here.
@csrf_exempt
def list(request):
	if request.method == "GET":
		manufacturers = Manufacturers.objects.all()
		results = [ob.as_json() for ob in manufacturers]
		result = {"count": Manufacturers.objects.count(), "manufacturers": results}
		return HttpResponse(json.dumps(result))
	return HttpResponse("Ok")

@csrf_exempt
def remove(request):
	if request.method == "POST":
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		manufacturer_id = data["manufacturer_id"]
		post_data = {"session_key": session_key}
		headers = {'Content-type': 'application/json'}		
		check = requests("http://localhost:8000/session/check", data=post_data, headers=headers)
		if check.status_code == requests.codes.ok:
			try:
				manufacturer = Manufacturers.objects.get(pk=manufacturer_id)
				manufacturer.delete()
			except ObjectDoesNotExist:
				with open(settings.STATIC_ROOT + '/jsons/manufacturer_not_found.json') as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=404)
		else:
			with open(settings.STATIC_ROOT + '/jsons/error_check.json') as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=401)
		
	return HttpResponse("Ok")

@csrf_exempt
def add(request):
	return HttpResponse("Ok")