
from django.urls import path
from .views import UserRegistration, UserLogin, UserProfileView, UserChangePasswordView
from .views import UserRegistration, UserLogin, UserProfile
from django.urls import path,include
from .views import UserRegistration, UserLogin, UserChangePasswordView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),

    path('profile/',UserProfileView.as_view(),name='profile'),
    path('change_password/',UserChangePasswordView.as_view(),name='change_password'),

    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('', UserProfile.as_view({'get': 'list'}), name='users'),
    path('<int:pk>', UserProfile.as_view({'get': 'retrieve', 'put': 'partial_update'}), name='user-detail'),

    path('change_password/',UserChangePasswordView.as_view(),name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
