from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Index.as_view()),
    path('sell/apartment/', ApartmentSell.as_view(), name='apartment_sell'),
    path('sell/room/', RoomSell.as_view(), name='room_sell'),
    path('sell/garage/', GarageSell.as_view(), name='garage_sell'),
    path('sell/land_plot/', LandPlotSell.as_view(), name='land_plot_sell'),
    path('rent/apartment/', ApartmentRent.as_view(), name='apartment_rent'),
    path('rent/room/', RoomRent.as_view(), name='room_rent'),
    path('rent/garage/', GarageRent.as_view(), name='garage_rent'),
    path('ad/<str:slug>/', AdDetail.as_view(), name='ad_detail')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#
# urlpatterns = [
#     path('', Index.as_view(), name='index'),
#     path('profile/<str:username>/', update_profile, name='profile'),
#     path('signup/', SignUp.as_view(), name='signup'),
#     path('accounts/', include('django.contrib.auth.urls')),
# ]


# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.views.generic import View, CreateView, DetailView
#
# from django.shortcuts import get_object_or_404
#
# from django.contrib.auth.decorators import login_required
# from django.db import transaction
# from django.contrib import messages
#
# from django.urls import get_resolver
#
# from .forms import *
# from .models import Profile


# class Index(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             user_profile = Profile.objects.get(user__pk=request.user.id)
#             return render(request, 'index.html', context={'profile': user_profile})
#         else:
#             return render(request, 'index.html')
#
#
# class SignUp(CreateView):
#     template_name = 'registration/signup.html'
#     form_class = RegisterForm
#     success_url = 'profile/<str:username>/'
#
#     def form_valid(self, form):
#         valid = super(SignUp, self).form_valid(form)
#         username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
#         new_user = authenticate(username=username, password=password)
#         login(self.request, new_user)
#         return valid
#
#     def get_success_url(self):
#         return reverse('profile', args=(self.object.username,))

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#     if user_form.is_valid():
#     # Создаем нового пользователя, но пока не сохраняем в базу данных.
#         new_user = user_form.save(commit=False)
#     # Задаем пользователю зашифрованный пароль.
#         new_user.set_password(user_form.cleaned_data['password'])Регистрация и профили пользователей  111
#     # Сохраняем пользователя в базе данных.
#         new_user.save()
#         return render(request, 'account/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request,'account/register.html',{'user_form': user_form})


# class UserProfile(DetailView):
#     model = User
#     slug_field = "username"
#     template_name = "profile.html"
#
#     def get_object(self):
#         object = get_object_or_404(User, username=self.kwargs.get("username"))
#         if self.request.user.username == object.username:
#             return object
#         else:
#             print("you are not the owner!!")


# @transaction.atomic
# @login_required
# def update_profile(request, username):
#     if request.method == 'POST':
#         # user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Profile updated successfully')
#         else:
#             messages.error(request, 'Error updating your profile')
#     else:
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profile.html', {'profile_form': profile_form})


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#         else:
#             form = LoginForm()
#             return render(request, 'account/login.html', {'form': form})