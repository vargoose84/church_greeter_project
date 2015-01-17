from django.conf.urls import patterns, url
from greeter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^getChurch/$', views.getChurch, name='getChurch'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^addGoer/$',views.addGoer, name='addgoer'),
    url(r'^getChurch/(?P<goerID>\w+)$', views.getBio, name = 'getBio'),
)