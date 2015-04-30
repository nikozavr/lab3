from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
	return HttpResponse("Ok")

@csrf_exempt
def add(request):
	return HttpResponse("Ok")