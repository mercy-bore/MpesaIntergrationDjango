from django.conf.urls.static import static
from rest_framework import routers
from django.urls import re_path,include
from . import views
from django.conf import settings

'''
The urls and API endpoints
'''

urlpatterns=[
    re_path(r'^api/photographers/$', views.Photographers.as_view()), #api endpoint  for all photographers
    re_path(r'^api/users/$', views.Users.as_view()), #api endpoint  for all users

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)