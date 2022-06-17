from wsgiref import validate
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email','first_name' ,'last_name','is_client', 'is_photographer']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone_number']


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email','phone_number', 'type', 'country', 'region']


class ClientSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        # write_only=True,
        required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2',
                  'first_name', 'last_name',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"passwordError": "Password fields did not match!"})
        return attrs

    def create(self, validated_data):
        client = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'], last_name=validated_data['last_name'],
          )

        client.set_password(validated_data['password'])
        client.is_client=True
        if client.save():
            Client.objects.create(client=client)
            raise serializers.ValidationError(
                {"successFULL": "Successfully saved!"})
        return client
       
class PhotographerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        # write_only=True,
        required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2',
                  'first_name', 'last_name',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"passwordError": "Password fields did not match!"})
        return attrs

    def create(self, validated_data):
        photographer = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        photographer.set_password(validated_data['password'])
        photographer.is_photographer=True
        if photographer.save():
            Photographer.objects.create(photographer=photographer)
            raise serializers.ValidationError(
                {"successFULL": "Successfully saved!"})
        return photographer
   
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'email', 'phone_number', 'question')
