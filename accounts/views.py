from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
from accounts.serializer import UserRegistrationSerializer


class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"msg": "done"},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
