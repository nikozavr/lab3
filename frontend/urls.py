from django.conf.urls import include, url

from frontend import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/', views.login, name="login"),
	url(r'^session/', include('session.urls', namespace="session")),
	url(r'^register/', views.register, name="register"),
#	url(r'^$', views.index, name='index'),
]
