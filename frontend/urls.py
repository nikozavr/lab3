from django.conf.urls import include, url

from frontend import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^$', views.index, name='index'),
]
