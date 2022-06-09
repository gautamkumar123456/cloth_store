from rest_framework import serializers
from .models import User

"""
Here we mainly used ModelSerializer.We use this because it is simple to use when we have to serialize the data present
in our model. We get all data from our model by default.
"""


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    """
    write_only come in use when we update and create instance.This field is not going to serialize. 
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    """
    This method is used to validate our data which we use in this serializer class.
    """

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password dosen't match")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ['email', 'password']


"""
This serializer is used for viewing Profile
"""


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_no', 'email']
