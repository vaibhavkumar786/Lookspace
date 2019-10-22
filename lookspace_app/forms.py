from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.db import transaction
from django.forms import ModelForm
from .models import SpaceDetails
from django import forms


class PartnerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_partner = True
        if commit:
            user.save()
        return user

class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user


class SpaceDetailsForm(ModelForm):

    class Meta:
        model = SpaceDetails
        fields = ('space_type', 'seater', 'total_quantity','time', 'price')

# class ScheduleVisit(forms.ModelForm):


