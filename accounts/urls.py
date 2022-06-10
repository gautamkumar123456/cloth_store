from django.urls import path
from .views import UserRegistration, UserLogin, UserProfile

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('', UserProfile.as_view({'get': 'list'}), name='users'),
    path('<int:pk>', UserProfile.as_view({'get': 'retrieve', 'put': 'partial_update'}), name='user-detail'),
]
