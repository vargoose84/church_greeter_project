from django.conf.urls import patterns, url
from greeter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^getChurch/$', views.getChurch, name='getChurch'),
    url(r'^getChurch/?type=all$', views.getChurch,{'listType' : 'all'} ,name='getChurchAll'),
    url(r'^getChurch/?type=unlearned$', views.getChurch,{'listType' : 'unlearned'} ,name='getChurchUnlearned'),
    url(r'^getChurch/?type=learned$', views.getChurch,{'listType' : 'learned'} ,name='getChurchLearned'),
    url(r'^getChurch/?type=reset$', views.getChurch,{'listType' : 'reset'} ,name='getChurchReset'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^addGoer/$',views.addGoer, name='addgoer'),
    url(r'^getChurch/(?P<goerID>\w+)/$', views.getBio, name = 'getBio'),
    url(r'^modifyGoer/(?P<goerID>\w+)/$', views.modifyGoer, name = 'modifyGoer'),
    url(r'^greeterRecordChange/(?P<goerID>\w+)/$',views.greeterRecordChange, name='greeterRecordChange'),
    url(r'^quiz/$',views.quiz, name='quiz'),
    url(r'^postSuggestion/$',views.postSuggestion, name='postSuggestion'),
    url(r'^viewSuggestions/$',views.viewSuggestions, name='viewSuggestions'),
    
)   