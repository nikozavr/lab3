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
	return HttpResponse("Ok")

@csrf_exempt
def add(request):
	return HttpResponse("Ok")