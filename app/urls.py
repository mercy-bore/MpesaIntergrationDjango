

from django.conf.urls.static import static
from rest_framework import routers
from django.urls import re_path, path, include
from . import views
from django.conf import settings
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', views.AllEvents, basename='events')
router.register(r'feedback', views.AllFeedback, basename='feedback')
router.register(r'portfolios', views.AllPortfolios, basename='portfolios')
router.register(r'photos', views.AllPhotos, basename='photos')
router.register(r'users', views.AllUsers, basename='users')
router.register(r'clients', views.AllClients, basename='clients')
router.register(r'rating', views.RatingView, basename='rating')
router.register(r'signup',views.ClientSignupView, basename='signup')
router.register(r'watermarks', views.WatermarksView, basename='watermarks')
router.register(r'homepage', views.HomepageView, basename='homepage')
router.register(r'photographers', views.AllPhotographers,
                basename='photographers')

'''
The urls and API endpoints
'''

urlpatterns = [
    path('api/', include(router.urls)),
    path('upload/portfoliophotos/', FileUploadView.as_view(), name='file-upload'),
    re_path('signup/photographer/new/', PhotographerSignupView.as_view()),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
