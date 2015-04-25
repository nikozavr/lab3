from django.shortcuts import render

# Create your views here.
def index(request):
	if request.method == "POST":
		json = json.loads(request.body)
	
	return HttpResponse("OK")