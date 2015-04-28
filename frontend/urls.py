from django.conf.urls import include, url

from frontend import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
#	url(r'^$', views.index, name='index'),
]
