from django.db import models

# Create your models here
class User(models.Model):
    '''
    This is a user model that has all the information about the user
    '''
    first_name =  models.CharField(max_length = 149, default = 'first name')
    last_name = models.CharField(max_length = 149, default = 'last name')
    password = models.CharField(max_length = 29, default = 'password')
    phone_number  = models.IntegerField(default = 254712345677)
    email = models.EmailField(max_length = 30, default =  'piczangu@gmail.com')

class Photographer(models.Model):
    '''
    This is a photographer model with the information about the photograher
    '''
    first_name =  models.CharField(max_length = 149 , default = 'first name')
    last_name = models.CharField(max_length = 149, default = 'last name')
    username = models.CharField(max_length = 29, default = 'username')
    password = models.CharField(max_length = 29, default = 'password')
    phone_number  = models.IntegerField(default = 254712345677)
    email = models.EmailField(max_length = 29, default = 'piczangu@gmail.com')
    profile_picture  = models.ImageField(upload_to = 'images/', default = 'image.jpg')
    website  = models.URLField(max_length = 199, blank = True)

class Event(models.Model):
    code = models.IntegerField(default = 1234)
    name = models.CharField(max_length = 30, default = 'Alumni Event')
    Location = models.CharField(max_length = 100, default = 'Nairobi,Kenya')
    date  = models.DateField( auto_now_add=True)
    price = models.FloatField()
    status  = models.BooleanField()
    noOfPhotos = models.IntegerField(default = 5)
    photos = models.ImageField(default = 'image.jpeg')
    photographer  = models.ForeignKey(Photographer, on_delete=models.CASCADE)

class Rating(models.Model):
    photograher = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    stars = models.IntegerField()
    

    
     

    

