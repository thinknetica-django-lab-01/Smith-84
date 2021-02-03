from django import forms
from .models import User, Profile
from django.core.exceptions import ValidationError


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
