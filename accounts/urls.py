from django.urls import path
from .views import UserRegistration, UserLogin, UserProfileView, UserChangePasswordView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('change_password/',UserChangePasswordView.as_view(),name='change_password'),
]
