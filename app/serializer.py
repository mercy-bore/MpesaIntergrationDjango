from rest_framework import serializers
from .models import Photographer,User,Event,Photos,Feedback,PhotographerAccount

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ('id','first_name','last_name','email')

class BuyerSerializer(serializers.ModelSerializer):
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

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id','email','phone_number','question')