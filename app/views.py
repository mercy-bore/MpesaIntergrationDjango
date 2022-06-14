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
from django.http import request,Http404
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class  PhotographerView(APIView):
    def get(self,request,format=None):
        all_photographers = Photographer.objects.all()
        serializers = PhotographerSerializer(all_photographers, many=True)
        return Response(serializers.data)
    
    def get_photographer(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            return Photographer.objects.get(pk=pk)
        except Photographer.DoesNotExist:
            return Http404
        
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        photographer = self.get_photographer(pk)
        serializers = PhotographerSerializer(photographer)
        return Response(serializers.data)
    
    def put(self, request, pk, format=None):
        photographer = self.get_photographer(pk)
        serializers = PhotographerSerializer(photographer, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        photographer = self.get_photographer(pk)
        photographer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class  ClientView(APIView):
    def get(self,request,format=None):
        all_clients = Client.objects.all()
        serializers = ClientSerializer(all_clients, many=True)
        return Response(serializers.data)
    
    def get_client(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Http404
        
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        client = self.get_client(pk)
        serializers = ClientSerializer(client)
        return Response(serializers.data)
    
    def put(self, request,*args, **kwargs):
        pk = self.kwargs.get('pk')
        client = self.get_client(pk)
        serializers = ClientSerializer(client,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        client = self.get_client(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
       
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

class Events(APIView):
    def get(self, request,format=None):
        events = Event.objects.all()
        serializers = EventSerializer(events, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        media_type = 'image/'
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

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

