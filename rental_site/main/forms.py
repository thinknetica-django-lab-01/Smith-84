from django import forms
from django.contrib.auth.models import User
from .models import Ad, Apartment, Room, Garage, LandPlot, Profile, Subscribers, Region
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age', 'phone_number',)

    def clean_age(self):
        current_age = self.cleaned_data['age']
        if int(current_age) < 18:
            raise ValidationError('Вы слишком молоды')

        return current_age


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('region', 'description', 'cost', 'address', 'action', 'custom_tags', )


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


class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = '__all__'


class SearchApartmentForm(forms.Form):
    ROOM_CHOICES = ([
        ('', '-'),
        ('1', '1-комнатные'),
        ('2', '2-комнатные'),
        ('3', '3-комнатные'),
        ('4', '4-комнатные и более')
    ])
    BUILDING_CHOICES = ([
        ('', '-'),
        ('new', 'Новостройка'),
        ('second', 'Вторичка')
    ])
    PRICE_RANGE = ([
        ('', '-'),
        ('1000000', 'до 1млн рублей'),
        ('2000000', 'от 1 до 2млн рублей'),
        ('3000000', 'От 2 до 3млн рублей'),
        ('5000000', 'От 3 до 5 млн рублей'),
        ('max', 'Более 5 млн рублей')
    ])

    room_count = forms.ChoiceField(required=True, choices=ROOM_CHOICES, label='Количество комнат')
    action = forms.ChoiceField(required=True, choices=BUILDING_CHOICES, label='Тип жилья')
    price = forms.ChoiceField(required=True, choices=PRICE_RANGE, label='Стоимость')
    region = forms.ModelChoiceField(required=True, queryset=Region.objects.all(), label='Населенный пункт')

    room_count.widget.attrs.update({'class': 'form-control', 'id': 'ptypes'})
    action.widget.attrs.update({'class': 'form-control', 'id': 'lookingfor'})
    price.widget.attrs.update({'class': 'form-control', 'id': 'price'})
    region.widget.attrs.update({'class': 'form-control', 'id': 'location'})


class SearchForm(forms.Form):
    search = forms.CharField(required=True)
    search.widget.attrs.update({'class': 'form-control', 'id': 'search'})
