from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< HEAD
from accounts.serializer import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer
=======
from .models import User
from accounts.serializer import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
>>>>>>> update_profile


# generating custom token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.


class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token": token, "msg": "done"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}},
                                status=status.HTTP_400_BAD_REQUEST)


<<<<<<< HEAD
class UserProfileView(APIView):
    '''
    IsAuthenticated class used for verifying that user is must for this specified operation
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UserChangePasswordView(APIView):
    '''
       IsAuthenticated class used for verifying that user is must for this specified operation
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


=======
""""
Using IsOwner class to implement in our UserProfile class to access only by authorized user.
"""


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


"""
This is userprofile class in which we use ModelViewset. In this class we use different-different methods
as per our requirement.  
"""


class UserProfile(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        return super(UserProfile, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserProfile, self).retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(UserProfile, self).partial_update(request, *args, **kwargs)
>>>>>>> update_profile
