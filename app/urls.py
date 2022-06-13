from django.conf.urls.static import static
from rest_framework import routers
from django.urls import re_path,include
from . import views
from django.conf import settings
from .views import ( CustomAuthToken, LogoutView, ClientSignupView,PhotographerSignupView)
from rest_framework import routers

'''
The urls and API endpoints
'''

urlpatterns=[
    # re_path('adduser/', ReigsterView.as_view()),
    re_path('login/', CustomAuthToken.as_view(), name='auth-token'),
    re_path('logout/', LogoutView.as_view(), name='logout-view'), 
    re_path('signup/client/', ClientSignupView.as_view()),
    re_path('signup/photographer/', PhotographerSignupView.as_view()),
    # re_path(r'^api/photographers/$', views.Photographer.as_view()), #api endpoint  for all photographers
    # re_path(r'^api/users/$', views.Users.as_view()), #api endpoint  for all users
    re_path(r'^api/events/$', views.Events.as_view()),  #api endpoint  for all events
    re_path(r'^api/photos/$', views.PhotosList.as_view()),  #api endpoint  for all photos

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)