from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	return HttpResponse("OK")

def index(request):
	return HttpResponse("OK")

def check_user(request):
	post_data = {""}

def requests_manager(request):
	return HttpResponse("OK")