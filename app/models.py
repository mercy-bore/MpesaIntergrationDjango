from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
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
    user_id=models.OneToOneField(User,related_name="client",on_delete=models.CASCADE)
    username=models.CharField(max_length=30)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=40)
    location = models.CharField(max_length = 30)
    phone_number=models.IntegerField(null=True)
    password = models.CharField(max_length= 30)
    password2 = models.CharField(max_length =30)
    

    def __str__(self):
        return str(self.username)
      
    def save_user(self):
        self.save()
        
class Photographer(models.Model):
    '''
    This is a photographer model with the information about the photographer
    '''
    user_id=models.OneToOneField(User, related_name="photographer", on_delete=models.CASCADE)
    username=models.CharField(max_length =30)
    first_name=models.CharField(max_length =30)
    last_name=models.CharField(max_length = 30)
    email=models.EmailField(max_length = 30)
    phone_number  = models.IntegerField( null=True)
    type=models.CharField(max_length =30,blank=True)
    country=models.CharField(max_length =30,blank=True)
    region=models.CharField(max_length = 30,blank=True)

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
    event_code = models.IntegerField(default = 1234)
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
    photographer_id = models.ForeignKey(Photographer,related_name="rating", on_delete=models.CASCADE,null=False,blank=False)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    user_id = models.OneToOneField(User,related_name="user",on_delete=models.CASCADE)


    def __str__(self):
          return  self.photographer_id
    
class Portfolio(models.Model):
    '''
    This is a portfolio model. It stores the photos of the photographer per category e.g wedding, wildlife, etc
    '''
    photographer_id = models.ForeignKey(Photographer,  on_delete= models.CASCADE)
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
    photograher_id = models.ForeignKey(Photographer,  on_delete = models.CASCADE)
    sales_amount = models.IntegerField()
    orders = models.IntegerField()
    downloads = models.IntegerField()
    customers = models.IntegerField()

class BoughtPhotos(models.Model):
    '''
    This model stores  information about photos that have been bought e.g  number of photos
    '''
    photographer_id =  models.ForeignKey(Photographer, on_delete = models.CASCADE)
    transaction_number = models.CharField(max_length = 70)
    date = models.DateField()
    phone_number = models.IntegerField()
    total_amount = models.IntegerField()
    noOfPhotos = models.IntegerField()
class Photos(models.Model):
    '''
    This models stores the information of the photos being uploaded by the photographers
    '''
    photographer_id = models.ForeignKey(Photographer,  on_delete = models.CASCADE)
    name = models.CharField(max_length = 30,default='John', )
    image = models.ImageField(upload_to = 'photos')
    price = models.FloatField()
    category = models.CharField(max_length = 30)

class Category(models.Model):
    photographer_id = models.ForeignKey(Photographer,  on_delete = models.CASCADE)
    files = models.ImageField(upload_to = 'categories')
class HelpForm(models.Model):
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

class HomepagePhotos(models.Model):
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

class Cart(models.Model):
    user=models.OneToOneField(User, related_name="cart", on_delete=models.CASCADE)
    photo_id = models.ForeignKey(Photos, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()

# ! mpesa models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# M-pesa Payment models
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'
class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'
class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name

class B2CPayment(BaseModel):
    ResultDesc = models.TextField()
    TransactionId = models.TextField()
    TransactionReceipt = models.TextField()
    TransactionAmount = models.IntegerField()
    TransactionCompletedDateTime = models.TextField()
    ReceiverPartyPublicName = models.TextField()
  
    class Meta:
        verbose_name = 'B2C Payment'
        verbose_name_plural = 'B2C Payments'
    def __str__(self):
        return self.ReceiverPartyPublicName
    
STATUS = ((1, "Pending"), (0, "Complete"))

class Transaction(models.Model):
    """This model records all the mpesa payment transactions"""
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return f"{self.transaction_no}"
class Earnings(models.Model):
    photographer = models.ForeignKey(Photographer,  on_delete = models.CASCADE)
    amount = models.IntegerField()
    b2ctransaction  = models.ForeignKey(B2CPayment,  on_delete = models.CASCADE)
