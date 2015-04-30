from django.conf.urls import include, url

from session import views

urlpatterns = [
	url(r'^create/$', views.create, name='create'),	
	url(r'^creck/$', views.check, name='check'),	
	url(r'^refresh/$', views.refresh, name='refresh'),
	url(r'^userinfo/$', views.userinfo, name='userinfo'),
]