from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^logtout$', views.logout, name="logout"),
    url(r'^add$', views.add, name="add"),
    url(r'^info/(?P<id>\w+)/$', views.info, name="info"),
    url(r'^create$', views.create, name="create"),
    url(r'^join/(?P<id>\w+)/$', views.join, name="join"),
]
