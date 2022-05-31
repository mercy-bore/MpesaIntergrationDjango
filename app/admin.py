from django.contrib import admin
from .models import User,Photographer,Event,Rating

# Register your models here

admin.site.register(User)
admin.site.register(Photographer)
admin.site.register(Event)
admin.site.register(Rating)