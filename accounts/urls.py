from django.urls import path
from .views import (UserRegistration, UserLogin, UserChangePasswordView, ResetPasswordConfirmView,
                    ResetPasswordValidateView, ResetPasswordTokenView, PartialUpdate, ViewProfile,
                    DestroyProfile, UserProfile)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('', UserProfile.as_view({'get': 'list'}), name='users'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('validate/', ResetPasswordValidateView.as_view()),
    path('password_reset/confirm/', ResetPasswordConfirmView.as_view(), name="password-reset-confirm"),
    path('password_reset/', ResetPasswordTokenView.as_view()),
    path('profile_delete/<int:pk>', DestroyProfile.as_view({'delete': 'destroy'})),
    path('profile_retrieve/<int:pk>', ViewProfile.as_view({'get': 'retrieve'})),
    path('profile_update/<int:pk>', PartialUpdate.as_view({'put': 'partial_update'}))
]
