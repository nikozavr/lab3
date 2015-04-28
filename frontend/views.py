from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests

# Create your views here.
def home(request):
	return HttpResponse("OK")

@csrf_exempt
def index(request):
	post_data = {"login":"nikozavr",
				"password":"nikitos1"}

	r, correct = requests.post("http://localhost:8000/session/", data=post_data) 
	#return HttpResponse("Bad")
	if correct == 1:
		return JsonResponse(r.json())
	else:
		return HttpResponse("Bad")

def check_user(request):
	post_data = {""}
	return HttpResponse("Ok")

def requests_manager(request):
	return HttpResponse("OK")