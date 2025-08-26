from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    email = serializers.EmailField(
        write_only=True,
        required=True,
          validators=[UniqueValidator(queryset=User.objects.all(), message="This email address is already in use.")]
    )
    username = serializers.CharField(required = True ,validators=[UniqueValidator(queryset=User.objects.all(), message="This username is already in use.")]
)
    class Meta:
        model = User
        fields = ('username', 'email', 'password' , 'confirm_password')
    def validate(self , data ) :
      password = data.get('password')
      confirm_password = data.get('confirm_password')
      if password != confirm_password:
        raise serializers.ValidationError("Passwords do not match!")
      return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password= validated_data['password'],
            email=validated_data['email']
        )
        return user