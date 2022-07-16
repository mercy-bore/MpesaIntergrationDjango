from wsgiref import validate
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


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
        user.is_photographer=True
        user.save()
        Photographer.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')


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

class HomepagePhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepagePhotos
        fields = '__all__'
        
class WatermarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watermarks
        fields = '__all__'


class HelpFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpForm
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
        photographer_id = validated_data['photographer_id']
        file = validated_data.pop('file')
        image_list = []
        for img in file:
            photo = Portfolio.objects.create(
                file=img, category=category, photographer_id=photographer_id)
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
class C2BPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = '__all__'
class B2CPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2CPayment
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class EarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earnings
        fields = '__all__'
class MpesaCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "phone_number",
            "amount",
            "reference",
            "description",
        )
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
class MpesaCallBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
#     xxxxxxxxxxxxxxxxxxxxxxxxxx
from .validators import validate_possible_number

from . import models
from .error_codes import ValidationError


class MpesaCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            "phone_number",
            "amount",
            "reference",
            "description",
        )

    def validate_phone_number(self, phone_number):
        """A very Basic validation to remove the preciding + or replace the 0 with 254"""
        if phone_number[0] == "+":
            phone_number = phone_number[1:]
        if phone_number[0] == "0":
            phone_number = "254" + phone_number[1:]
        try:
            validate_possible_number(phone_number, "KE")
        except:
            raise serializers.ValidationError({"error": "Phone number is not valid"})

        return phone_number

    def validate_amount(self, amount):
        """this methods validates the amount"""
        if not amount or float(amount) <= 0:
            raise serializers.ValidationError(
                {"error": "Amount must be greater than Zero"}
            )
        return amount

    def validate_reference(self, reference):
        """Write your validation logic here"""
        if reference:
            return reference
        return "Test"

    def validate_description(self, description):
        """Write your validation logic here"""
        if description:
            return description
        return "Test"
class MpesaB2CCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.B2CTransaction
        fields = (
            "phone_number",
            "amount",
            "reference",
            "description",
        )

    def validate_phone_number(self, phone_number):
        """A very Basic validation to remove the preciding + or replace the 0 with 254"""
        if phone_number[0] == "+":
            phone_number = phone_number[1:]
        if phone_number[0] == "0":
            phone_number = "254" + phone_number[1:]
        try:
            validate_possible_number(phone_number, "KE")
        except:
            raise serializers.ValidationError({"error": "Phone number is not valid"})

        return phone_number

    def validate_amount(self, amount):
        """this methods validates the amount"""
        if not amount or float(amount) <= 0:
            raise serializers.ValidationError(
                {"error": "Amount must be greater than Zero"}
            )
        return amount

    def validate_reference(self, reference):
        """Write your validation logic here"""
        if reference:
            return reference
        return "Test"

    def validate_description(self, description):
        """Write your validation logic here"""
        if description:
            return description
        return "Test"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"
class B2CTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.B2CTransaction
        fields = "__all__"