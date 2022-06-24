from wsgiref import validate
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'is_client', 'is_photographer']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone_number']


class PhotographerSerializer(serializers.ModelSerializer):
    rating = serializers.StringRelatedField(many=True)

    class Meta:
        model = Photographer
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone_number', 'type', 'country', 'region','rating']


class ClientSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_client=True
        user.save()
        Client.objects.create(user=user)
        return user

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

    def save(self, **kwargs):
        user = User.objects.create(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'], 
            last_name=self.validated_data['last_name']
            )
        user.set_password('password')
        user.is_photographer = True
        if user.save():
            Photographer.objects.create(user=user)
            raise serializers.ValidationError(
                {"successFULL": "Successfully saved!"})
        return user


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

class HomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homepage
        fields = '__all__'
        
class WatermarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watermarks
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'email', 'phone_number', 'question')


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.ListField(
    child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False))

    class Meta:
        model = Portfolio
        fields = '__all__'

    def create(self, validated_data):
        category = validated_data['category']
        photographer = validated_data['photographer']
        file = validated_data.pop('file')
        image_list = []
        for img in file:
            photo = Portfolio.objects.create(
                file=img, category=category, photographer=photographer)
            imageurl = f'{photo.file.url}'
            image_list.append(imageurl)
        return image_list


class FileUploadDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
