from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
# Create your models here

class User(AbstractUser):
  #Boolean fields to select the type of account.
    is_client = models.BooleanField(default=False) 
    is_photographer = models.BooleanField(default=False)
  
    def __str__(self):
        return (self.username) 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Client(models.Model):
    '''
    This is a user model that has all the information about the user
    '''
    user=models.OneToOneField(User, related_name="client", on_delete=models.CASCADE)
    first_name =  models.CharField(max_length = 20 , default = 'first name',null=True)
    last_name = models.CharField(max_length = 20, default = 'last name',null=True) 
    phone_number  = models.IntegerField( null=True)

    def __str__(self):
        return str(self.first_name) 
      
    def save_user(self):
        self.save()
class Photographer(models.Model):
    '''
    This is a photographer model with the information about the photographer
    '''
    user=models.OneToOneField(User, related_name="photographer", on_delete=models.CASCADE)
    first_name =  models.CharField(max_length = 149 , default = 'first name',blank=True)
    last_name = models.CharField(max_length = 149, default = 'last name',blank=True)
    phone_number  = models.IntegerField(default='0729275511', blank=True)
    profile_picture  = models.ImageField(upload_to = 'images/', default = 'image.jpg',blank=True)
    website  = models.URLField(max_length = 30, null = True)

    def __str__(self):
        return str(self.user.username)
      
    def save_photographer(self):
        self.save()

    @classmethod
    def search_by_first_name(cls,search_term):
        photographer = cls.objects.filter(first_name__icontains=search_term)
        return photographer
class Event(models.Model):
    '''
    This is the event model with the information about the event, including when it will be the location etc
    '''
    code = models.IntegerField(default = 1234)
    name = models.CharField(max_length = 30, default = 'Alumni Event')
    location = models.CharField(max_length = 100, default = 'Nairobi,Kenya')
    date  = models.DateField( auto_now_add=True)
    price = models.FloatField()
    status  = models.BooleanField()
    noOfPhotos = models.IntegerField(default = 5)
    photos = models.ImageField(upload_to='sale/',default = 'image.jpeg')
    photographer  = models.ForeignKey(Photographer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
      
    def save_event(self):
        self.save()
  
class Rating(models.Model):
    '''
    This is a rating model. It will allow a user to rate a photograher
    '''
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    stars = models.IntegerField()
    
class Portfolio(models.Model):
    '''
    This is a portfolio model. It stores the photos of the photographer per category e.g wedding, wildlife, etc
    '''
    photographer = models.ForeignKey(Photographer, on_delete= models.CASCADE)
    category = models.CharField(max_length = 30)
    images = models.ImageField()

    def __str__(self):
        return self.category
      
    def save_portfolio(self):
        self.save()
class PhotographerAccount(models.Model):
    '''
    This is a photographer's account  model. It stores account details of a photographer
    '''
    photograher = models.ForeignKey(Photographer, on_delete = models.CASCADE)
    sales_amount = models.IntegerField()
    orders = models.IntegerField()
    downloads = models.IntegerField()
    customers = models.IntegerField()

class BoughtPhotos(models.Model):
    '''
    This model stores  information about photos that have been bought e.g  number of photos
    '''
    photographer =  models.ForeignKey(Photographer, on_delete = models.CASCADE)
    transaction_number = models.CharField(max_length = 70)
    date = models.DateField()
    phone_number = models.IntegerField()
    total_amount = models.IntegerField()
    noOfPhotos = models.IntegerField()
class Photos(models.Model):
    '''
    This models stores the information of the photos being uploaded by the photographers
    '''
    photographer = models.ForeignKey(Photographer, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    image = models.ImageField(upload_to = 'photos')
    price = models.FloatField()
    category = models.CharField(max_length = 30)

class Feedback(models.Model):
    '''
    This model stores the details about the questions or feedback given by a user
    '''
    user =  models.ForeignKey(User, on_delete = models.CASCADE)
    email = models.EmailField(max_length = 30)
    phone_number = models.IntegerField()
    question = models.TextField()

    def __str__(self):
        return self.question
      
    def save_feedback(self):
        self.save()
    
class PhotoUsers(models.Model):
    '''
    This model stores information about photos bought by a specific user
    '''
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    photos = models.ForeignKey(Photos, on_delete = models.CASCADE) 


    
     

    

