from rest_framework import serializers
from .models import Photographer,User,Event,Photos,Feedback,PhotographerAccount

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ('id','first_name','last_name','email')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email') 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','name','location','price','noOfPhotos','photos')

class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ('id','name','image', 'price', 'category')