from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
