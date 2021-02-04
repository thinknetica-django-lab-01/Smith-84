from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.forms import generic_inlineformset_factory


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age', )

    def clean_age(self):
        current_age = self.cleaned_data['age']
        if int(current_age) < 18:
            raise ValidationError('Вы слишком молоды')

        return current_age


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class LandPlotForm(forms.ModelForm):
    class Meta:
        model = LandPlot
        fields = '__all__'


class GarageForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = '__all__'
