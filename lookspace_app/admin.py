from django.contrib import admin

# Register your models here.
from .models import SpaceDetails , User, BookedSeats, ScheduleVisit

admin.site.register(User)
admin.site.register(SpaceDetails)
admin.site.register(BookedSeats)
admin.site.register(ScheduleVisit)
