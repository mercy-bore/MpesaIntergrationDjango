from rest_framework import serializers
from .models import Photographer,User,

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ('id','first_name','last_name','email')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email') 
