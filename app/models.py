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
    '''
    This is the event model with the information about the event, including when it will be the location etc
    '''
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
    '''
    This is a rating model. It will allow a user to rate a photograher
    '''
    photograher = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    stars = models.IntegerField()
    
class Portfolio(models.Model):
    '''
    This is a portfolio model. It stores the photos of the photographer per category e.g wedding, wildlife, etc
    '''
    photographer = models.ForeignKey(Photographer, on_delete= models.CASCADE)
    category = models.CharField(max_length = 30)
    images = models.ImageField()

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
    This models stores the information of the photos being uploaded by the photogrphers
    '''
    photographer = models.ForeignKey(Photographer, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    image = models.ImageField(upload_to = 'photos')
    price = models.FloatField()
    category = models.CharField(max_length = 30)

class Feedback(models.Model):
    user =  models.ForeignKey(User, on_delete = models.CASCADE)
    email = models.EmailField(max_length = 30)
    phone_number = models.IntegerField()
    question = models.TextField()
    



    
     

    

