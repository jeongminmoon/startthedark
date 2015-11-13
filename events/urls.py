from django.conf.urls import patterns, include, url
from events import views

urlpatterns = patterns('',
	url(r'^tonight/$',views.tonight, name= 'ev_tonight'),
)
