from django.conf.urls.static import static
from rest_framework import routers
from django.urls import re_path,include
from . import views
from django.conf import settings
from .views import ( CustomAuthToken, LogoutView, ClientSignupView,PhotographerSignupView,PhotographerView, ClientView)
from rest_framework import routers

'''
The urls and API endpoints
'''

urlpatterns=[
    re_path('photographer-id/(?P<pk>[0-9]+)/',
        views.PhotographerView.as_view()),
    re_path(r'^client-id/(?P<pk>[0-9]+)/$',
        views.ClientView.as_view()),
    re_path('signup/client/new/', ClientSignupView.as_view()),
    re_path('signup/photographer/new/', PhotographerSignupView.as_view()),
    re_path('photographers/',PhotographerView.as_view()),
    re_path('clients/',ClientView.as_view()),
    re_path(r'^api/events/$', views.Events.as_view()),  #api endpoint  for all events
    re_path(r'^api/photos/$', views.PhotosList.as_view()),  #api endpoint  for all photos

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)