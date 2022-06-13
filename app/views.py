from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import *
from .serializer import *
from rest_framework.generics import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsClientUser, IsPhotographerUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView
from django.http import request
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class PhotographerSignupView(generics.GenericAPIView):
    serializer_class=PhotographerSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })


class ClientSignupView(generics.GenericAPIView):
    serializer_class=ClientSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_client':user.is_client,
            'is_photographer':user.is_photographer
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsClientUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user

class PhotographerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsPhotographerUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
# Create your views here.
# class Photographers(APIView):
#     def get(self, request,format=None):
#         photographers = Photographer.objects.all()
#         serializers = PhotographerSerializer(photographers, many=True)
#         return Response(serializers.data)
#     def post(self, request, format=None):
#         serializers = PhotographerSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)

#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# class Users(APIView):
#     def get(self, request,format=None):
#         users = User.objects.all()
#         serializers = BuyerSerializer(users, many=True)
#         return Response(serializers.data)
#     def post(self, request, format=None):
#         serializers = BuyerSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)

#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class Events(APIView):
    def get(self, request,format=None):
        events = Event.objects.all()
        serializers = EventSerializer(events, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = EventSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PhotosList(APIView):
    def get(self, request,format=None):
        photos = Photos.objects.all()
        serializers = PhotosSerializer(photos, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = PhotosSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    ###authentication
    

# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer=self.serializer_class(data=request.data, context={'request':request})
#         serializer.is_valid(raise_exception=True)
#         user=serializer.validated_data['user']
#         token, created=Token.objects.get_or_create(user=user)
#         return Response({
#             'token':token.key,
#             'user_id':user.pk,
#             'is_buyer':user.is_buyer,
#             'is_photographer':user.is_photographer
#         })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


# class ReigsterView(GenericAPIView):
#     serializer_class = BuyerSerializer

#     def post(self, request):
#         serializer = BuyerSerializer(data=request.data)

#         if serializer.is_valid():
#             user=serializer.save()
#             return Response({
#             "user":BuyerSerializer(user, context=self.get_serializer_context()).data,
#             "token":Token.objects.get(user=user).key,
#             "message":"account created successfully"
#         })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class GetUser(APIView):  
#     def get(self,request,id):
#         print(id)
#         if id:
#             user = get_object_or_404(User, id=id)

        
#             User_serializer = BuyerSerializer(user) 
        
#             return Response(User_serializer.data)

