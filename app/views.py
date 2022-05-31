from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User,Photographer
from .serializer import PhotographerSerializer,UserSerializer
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets

# Create your views here.
class Photographers(APIView):
    def get(self, request,format=None):
        photographers = Photographer.objects.all()
        serializers = PhotographerSerializer(photographers, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = PhotographerSerializer(post,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Users(APIView):
    def get(self, request,format=None):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = UserSerializer(post,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)