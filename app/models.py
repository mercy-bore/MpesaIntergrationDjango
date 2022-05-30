from django.db import models

# Create your models here
class User(models.Model):
    '''
    This is a user model that has all the information about the user
    '''
    first_name =  models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    password = models.CharField(max_length = 30)
    phone_number  = models.IntegerField(max_length = 12)
    email = models.EmailField(max_length = 30)

class Photographer(models.Model):
    first_name =  models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    password = models.CharField(max_length = 30)
    phone_number  = models.IntegerField(max_length = 12)
    email = models.EmailField(max_length = 30)
    profile_picture  = models.ImageField(upload_to = 'images/')


