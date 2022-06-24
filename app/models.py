from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
# Create your models here

class User(AbstractUser):
    is_client=models.BooleanField(default=False)
    is_photographer=models.BooleanField(default=False)

    def __str__(self) :
        return str(self.username)
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)    
        

class Client(models.Model):
    '''
    This is a user model that has all the information about the user
    '''
    user=models.OneToOneField(User,related_name="client", on_delete=models.CASCADE)
    username=models.CharField(max_length=40)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=40)
    phone_number=models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)
      
    def save_user(self):
        self.save()
        
class Photographer(models.Model):
    '''
    This is a photographer model with the information about the photographer
    '''
    user=models.OneToOneField(User, related_name="photographer", on_delete=models.CASCADE)
    username=models.CharField(max_length =30, default='John55')
    first_name=models.CharField(max_length =30, default='John')
    last_name=models.CharField(max_length = 30, default = 'Doe')
    email=models.EmailField(max_length = 30,default='john@gmail.com')
    phone_number  = models.IntegerField( null=True)
    type=models.CharField(max_length =30, default='wildlife',blank=True)
    country=models.CharField(max_length =30, default='Kenya',blank=True)
    region=models.CharField(max_length = 30, default = 'Africa',blank=True)

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
    price = models.FloatField(default=00.00)
    status  = models.BooleanField(default='False')
    noOfPhotos = models.IntegerField(default = 5)
    photos = models.ImageField(upload_to='sale/',default = 'image.jpeg')
    photographer  = models.ForeignKey(Photographer,related_name='photographer',on_delete=models.CASCADE)

    def __str__(self):
        return self.name
      
    def save_event(self):
        self.save()
  
class Rating(models.Model):
    '''
    This is a rating model. It will allow a user to rate a photograher
    '''
    photographer = models.ForeignKey(Photographer,related_name="rating", on_delete=models.CASCADE,null=False,blank=False)
    one = models.PositiveIntegerField(default=0, null=True, blank=True)
    two = models.PositiveIntegerField(default=0, null=True, blank=True)
    three = models.PositiveIntegerField(default=0, null=True, blank=True)
    four = models.PositiveIntegerField(default=0, null=True, blank=True)
    five = models.PositiveIntegerField(default=0, null=True, blank=True)
    user = models.OneToOneField(User,related_name="user",on_delete=models.CASCADE)

  

    def __str__(self):
    
          rating_list = {
            '1': self.one,
            '2': self.two,
            '3': self.three,
            '4': self.four,
            '5': self.five
          }
          return str(max(rating_list, key=rating_list.get))
    
class Portfolio(models.Model):
    '''
    This is a portfolio model. It stores the photos of the photographer per category e.g wedding, wildlife, etc
    '''
    photographer = models.ForeignKey(Photographer,  on_delete= models.CASCADE)
    category = models.CharField(max_length = 30)
    file= models.FileField(default='image.jpeg',upload_to='portfolio/')

    def __str__(self):
        return self.category
      
    def save_portfolio(self):
        self.save()
class PhotographerAccount(models.Model):
    '''
    This is a photographer's account  model. It stores account details of a photographer
    '''
    photograher = models.ForeignKey(Photographer,  on_delete = models.CASCADE)
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
    photographer = models.ForeignKey(Photographer,  on_delete = models.CASCADE)
    name = models.CharField(max_length = 30,default='John', )
    image = models.ImageField(upload_to = 'photos')
    price = models.FloatField()
    category = models.CharField(max_length = 30)

class Feedback(models.Model):
    '''
    This model stores the details about the questions or feedback given by a user
    '''
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
    photos = models.ForeignKey(Photos, on_delete = models.CASCADE) 

class Homepage(models.Model):
    '''
    This is a models that allows the admin to upload photos used in the homepage
    '''
    name  = models.CharField(max_length = 30)
    file = models.ImageField(default='image.jpeg',upload_to='homepage_photos/')

    def __str__(self):
        return self.name
      
    def save_homepage(self):
        self.save() 
class Watermarks(models.Model):
    '''
    This is a watermarks model. It stores the watermarked photos uploaded by the admin
    '''
    name = models.CharField(max_length = 30)
    file = models.ImageField(default='image.jpeg',upload_to='watermarks/')

    def __str__(self):
        return self.name
    def save_watermarks(self):
        self.save()
   