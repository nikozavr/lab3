from django.conf.urls import include, url

from backend_manufacturers import views

urlpatterns = [
	url(r'^list/$', views.list, name='list'),	
	url(r'^remove/$', views.remove, name='remove'),	
	url(r'^add/$', views.add, name='add'),	
]