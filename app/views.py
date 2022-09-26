
from cgi import print_directory
from django.http import  HttpResponse, JsonResponse
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import *
import base64
from rest_framework.decorators import api_view
from .serializer import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsClientUser, IsPhotographerUser
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment
import requests
import json
from decouple import config
import logging
from .stkpush import *
gateway = MpesaGateWay()
gatewayb = MpesaB2CPayment()

# ! Mpesa

def getAccessToken(request):
    consumer_key = 'JnHLddwQJBWIJ83GHePJ5irqNNqJ6Rjt'
    consumer_secret = 'cBc2TJOtQLD0zH3F'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254798670839,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254798670839,  # replace with your phone number to get stk push
        "CallBackURL": "https://764f-41-90-176-209.in.ngrok.io/callback",
        "AccountReference":"Piczangu",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)
    return HttpResponse('Success.STK push sent.',response)
    
@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://764f-41-90-176-209.in.ngrok.io/confirmation",
               "ValidationURL": "https://764f-41-90-176-209.in.ngrok.io/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    print(response.text)
    return HttpResponse(response.text)
 
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


def B2C(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    b2c_api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "InitiatorName": "testapi",
        "SecurityCredential":LipanaMpesaPpassword.SecurityCredential,
        "CommandID": "BusinessPayment",
        "Amount": 1,
        "PartyA": 600992,
        "PartyB": 254798670839,
        "Remarks": "Test remarks",
        "QueueTimeOutURL": "https://764f-41-90-176-209.in.ngrok.io/b2c/queue",
        "ResultURL": "https://764f-41-90-176-209.in.ngrok.io/b2c/result",
        "Occassion": "",
  }

    response = requests.post(b2c_api_url, json=request, headers=headers)
    print(response.text)
    return HttpResponse('Success.Transaction from Piczangu to client initiated.',response)
@csrf_exempt
def b2c_result(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context)) 

@csrf_exempt
def b2c_queue(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

    

       
# * end of mpesa
# * auth


#! end of auth
class FileUploadView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = FileUploadDisplaySerializer
    def post(self, request, format=None): 
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():    #validate the serialized data to make sure its valid       
            qs = serializer.save()                     
            message = {'detail':qs, 'status':True}
            return Response(message, status=status.HTTP_201_CREATED)
        else: #if the serialzed data is not valid, return erro response
            data = {"detail":serializer.errors, 'status':False}            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        return Portfolio.objects.all()



class AllUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class AllPhotographers(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

class AllClients(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

class AllEvents(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class AllPhotos(viewsets.ModelViewSet):  
    serializer_class = PhotosSerializer
    queryset = Photos.objects.all()

class HelpFormView(viewsets.ModelViewSet):
    serializer_class = HelpFormSerializer
    queryset = HelpForm.objects.all()
class AllPortfolios(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

class HomepagePhotosView(viewsets.ModelViewSet):
    serializer_class = HomepagePhotosSerializer
    queryset = HomepagePhotos.objects.all()
    
class WatermarksView(viewsets.ModelViewSet):
    serializer_class = WatermarksSerializer
    queryset = Watermarks.objects.all()
class RatingView(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
class EarningsView(viewsets.ModelViewSet):
    serializer_class = EarningsSerializer
    queryset = Earnings.objects.all()
class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

class B2CTransactionView(viewsets.ModelViewSet):
    serializer_class = B2CTransactionSerializer
    queryset = B2CTransaction.objects.all()

class PhotographerSignupView(generics.CreateAPIView):
    queryset = Photographer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PhotographerSignupSerializer

class ClientSignupView(generics.CreateAPIView):
    queryset = Client.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClientSignupSerializer
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_client': user.is_client,
            'is_photographer': user.is_photographer
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & IsClientUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PhotographerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & IsPhotographerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

#oooo

class MpesaCheckout(APIView):
    serializer = MpesaCheckoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payload = {"data":serializer.validated_data, "request":request}
            res = gateway.stk_push_request(payload)
            return Response(res, status=200)
class MpesaB2CCheckout(APIView):
    serializer = MpesaB2CCheckoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payload = {"data":serializer.validated_data, "request":request}
            res = gatewayb.b2c_request(payload)
            return Response(res, status=200)


class MpesaCallBack(APIView):
    def get(self, request):
        return Response(MpesaPayment.objects.all(), status=200)

    def post(self, request, *args, **kwargs):
        logging.info("{}".format("Callback from MPESA"))
        data = request.body
        return gateway.callback_handler(json.loads(data))
class MpesaB2CResponse(APIView):
    def get(self, request):
        return Response(B2CTransaction.objects.all(), status=200)

    def post(self, request, *args, **kwargs):
        logging.info("{}".format("Callback from MPESA"))
        data = request.body
        return gatewayb.b2c_callback_handler(json.loads(data))
    
