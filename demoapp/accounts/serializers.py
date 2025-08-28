from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
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
        required=True,
          validators=[UniqueValidator(queryset=User.objects.all(), message="Invalid Email!")]
    )
    username = serializers.CharField(required = True ,validators=[UniqueValidator(queryset=User.objects.all(), message="This username is already in use.")]
)
    class Meta:
        model = User
        fields = ('username', 'email', 'password' , 'confirm_password')
    def validate(self , data ) :
      password = data.get('password')
      confirm_password = data.get('confirm_password')
      password_validation(password , confirm_password)
      return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password= validated_data['password'],
            email=validated_data['email']
        )
        return user

class LogInSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        required=True,
    )
    username = serializers.CharField(required = True )

    class Meta:
        model = User
        fields = ('username','password' )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        print(username , password)
        # user = authenticate(request=self.context.get('request'), username=username, password=password)
        # print("user object : " , user)
        # if user is  None :
        #     raise serializers.ValidationError({"status": "error", "message": "Username or password doesn't match. Please try again."})

        # if not user.is_active:
        #     raise serializers.ValidationError({"status": "error", "message": "Account not verified."})
        return attrs



class ResetPasswordViaEmailSerializer(serializers.ModelSerializer):
    """
    Serializer for Password reset.
    """
    email = serializers.EmailField(
        required=True
    )
    class Meta:
        model = User
        fields = ('email',)
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            return attrs
        else :
            raise serializers.ValidationError("Invalid Email!")
class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    class Meta :
        model = User
        fields = ('password', 'confirm_password')
    def validate(self , data ) :
      password = data.get('password')
      confirm_password = data.get('confirm_password')
      password_validation(password , confirm_password)
      return data

    def update(self, instance, validated_data):
        user = User.objects.get(id=instance.id)
        user.set_password(validated_data['password'])
        user.save()
        return instance


def password_validation(password , confirm_password) :
    try:
          validate_password(password)
    except ValidationError as e:
            raise serializers.ValidationError(e.messages)
    if password != confirm_password:
        raise serializers.ValidationError("Passwords do not match!")


