from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phone_field import PhoneField

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)

CATEGORY_CHOICES = (
    ('INDIVIDUAL', 'INDIVIDUAL'),
    ('CABIN', 'CABIN'),
    ('CONFERENCE ROOM', 'CONFERENCE ROOM'),

)

class SpaceDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    space_type = models.CharField(choices=CATEGORY_CHOICES, max_length = 200, null = True, default="Other")
    seater = models.IntegerField(default=0 )
    total_quantity = models.IntegerField( default=0 )
    time = models.TimeField(default=timezone.now)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.space_type

class BookedSeats(models.Model):
    space = models.ForeignKey(SpaceDetails, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default= timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

class ScheduleVisit(models.Model):
    customer_name = models.CharField(max_length=64, null = True)
    email = models.EmailField(max_length = 128, null = True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    company_name = models.CharField(max_length=64, null= True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()

class ContactForm(models.Model):
    contact_name = models.CharField(max_length=64, null = True)
    email = models.EmailField(max_length = 128, null = True)
    message = models.CharField(max_length=64, null = True)




