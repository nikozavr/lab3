from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from backend_manufacturers.models import Manufacturers
import json

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
		user_id = int(session_key[:3])
		logger = logging.getLogger('lab3')
		s = cache.get(session_key)
		
	return HttpResponse("Ok")

@csrf_exempt
def add(request):
	return HttpResponse("Ok")