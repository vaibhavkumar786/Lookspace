from django.contrib import admin

# Register your models here.
from .models import SpaceDetails , User

admin.site.register(User)
admin.site.register(SpaceDetails)