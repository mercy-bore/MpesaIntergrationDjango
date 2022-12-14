

from django.conf.urls.static import static
from django.urls import re_path, path, include
from . import views
from django.conf import settings
from .views import *
from .stkpush import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = router.urls
router.register(r'events', views.AllEvents, basename='events')
router.register(r'feedback', views.HelpFormView, basename='feedback')
router.register(r'portfolios', views.AllPortfolios, basename='portfolios')
router.register(r'photos', views.AllPhotos, basename='photos')
router.register(r'users', views.AllUsers, basename='users')
router.register(r'clients', views.AllClients, basename='clients')
router.register(r'rating', views.RatingView, basename='rating')
# router.register(r'signup',views.ClientSignupView, basename='signup')
router.register(r'watermarks', views.WatermarksView, basename='watermarks')
router.register(r'homepage', views.HomepagePhotosView, basename='homepage')
# router.register(r'payment',views.Confirmation, basename='payment')
router.register(r'photographers', views.AllPhotographers,
                basename='photographers')
router.register(r'cart',views.CartView, basename='cart')
router.register(r'transactions',views.TransactionView, basename='transactions')
router.register(r'b2c/transactions',views.B2CTransactionView, basename='b2c/transactions')
router.register(r'earnings',views.EarningsView,basename='earnings')
'''
The urls and API endpoints
'''

urlpatterns = [
    path('api/', include(router.urls)),
    path('upload/portfoliophotos/', FileUploadView.as_view(), name='file-upload'),
    re_path('signup/photographer/new/', PhotographerSignupView.as_view()),
    re_path('signup/client/new/', ClientSignupView.as_view()),
    #! mpesa
    # path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
        # register, confirmation, validation and callback urls
    # path('callback',views.call_back,name = "callback"),
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    # path('c2b/confirmation', C2BPayments.as_view(), name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
  
    # b2c URLs   
    path('b2c/payment',views.B2C,name='payment'), 
    path('b2c/queue',views.b2c_queue, name= "queue"),
    path('b2c/result',views.b2c_result,name ='result'),
    # path('b2c/confirmation',B2CPayments.as_view(),name="confirmation"),
    
    path("checkout", views.MpesaCheckout.as_view(), name="checkout"),
    path("callback", views.MpesaCallBack.as_view(), name="callback"),
    path("b2c/checkout", views.MpesaB2CCheckout.as_view(), name="checkout"),
    path("b2c/callback", views.MpesaB2CResponse.as_view(), name="callback"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
