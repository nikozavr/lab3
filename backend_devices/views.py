from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from backend_devices.models import Devices
import json
# Create your views here.
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
		logger = logging.getLogger('lab3')
		logger.info("delete")
		data = request.body
		data = json.loads(data.decode('utf8'))
		session_key = data["session_key"]
		manufacturer_id = data["device_id"]
		post_data = {"session_key": session_key}
		headers = {'Content-type': 'application/json'}	
		logger.info("delete")	
		check = requests("http://localhost:8000/session/check", data=post_data, headers=headers)
		if check.status_code == requests.codes.ok:
			try:
				
				logger.info("delete")
				device = Devices.objects.get(pk=device_id)
				device.delete()
			except ObjectDoesNotExist:
				with open(settings.STATIC_ROOT + '/jsons/device_not_found.json') as data_file:    
					data = json.load(data_file)
				logger.info(data)
				return HttpResponse(json.dumps(data), status=404)
		else:
			with open(settings.STATIC_ROOT + '/jsons/error_check.json') as data_file:    
				data = json.load(data_file)
			logger.info(data)
			return HttpResponse(json.dumps(data), status=401)

@csrf_exempt
def add(request):
	return HttpResponse("Ok")