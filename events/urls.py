﻿from django.conf.urls import patterns, include, url
from events import views

urlpatterns = patterns('',
	url(r'^create/$', views.create, name = 'ev_create'),
	url(r'^tonight/$',views.tonight, name= 'ev_tonight'),
)
