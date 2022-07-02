
from django.http import  HttpResponse, JsonResponse
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import *
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
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference":"Piczangu",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('Success.STK push sent.',response)

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://2132-41-90-185-140.in.ngrok.io/confirmation",
               "ValidationURL": "https://2132-41-90-185-140.in.ngrok.io/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
class C2BPayments(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PaymentSerializer
    def post(self,request,format=None):
        mpesa_body =request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)
        payment = MpesaPayment.objects.create(
            first_name=mpesa_payment['first_name'], #FirstName  
            last_name=mpesa_payment['last_name'], #LastName
            middle_name=mpesa_payment['middle_name'], #MiddleName
            description=mpesa_payment['description'],#TransID
            phone_number=mpesa_payment['phone_number'], #MSISDN
            amount=mpesa_payment['amount'], #TransAmount
            reference=mpesa_payment['reference'], #BillRefNumber
            organization_balance=mpesa_payment['organization_balance'], #OrgAccountBalance
            type=mpesa_payment['type'], #TransactionType
        )   
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payments = serializer.save()
            qs = json.dumps(payments)
            context = {
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            }
            message = {'detail':qs, 'status':True, 'context':context}
            return Response(message, request.data,status=status.HTTP_201_CREATED)
        else: #if the serialzed data is not valid, return erro response
                data = {"detail":serializer.errors, 'status':False}            
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
            return MpesaPayment.objects.all()

    # return JsonResponse(dict(context))
# * end of mpesa
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

class AllFeedback(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
class AllPortfolios(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

class HomepageView(viewsets.ModelViewSet):
    serializer_class = HomepageSerializer
    queryset = Homepage.objects.all()
    
class WatermarksView(viewsets.ModelViewSet):
    serializer_class = WatermarksSerializer
    queryset = Watermarks.objects.all()
class RatingView(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()


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
