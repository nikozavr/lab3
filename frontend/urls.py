from django.conf.urls import include, url

from frontend import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/', views.login, name="login"),
	url(r'^logout/', views.logout, name="logout"),
	url(r'^register/', views.register, name="register"),

	url(r'^session/', include('session.urls', namespace="session")),
	url(r'^backend_manufacturers/', include('backend_manufacturers.urls', namespace="backend_manufacturers"))

#	url(r'^$', views.index, name='index'),
]
