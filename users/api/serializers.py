from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import authenticate

from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration.
    - Validates matching passwords.
    - Ensures email uniqueness.
    - Uses 'create_user' to securely hash passwords.
    """

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}, # Password is never sent back in JSON
            'email': {'required': True}
        }

    def validate(self, attrs):
        """
        Custom validation for registration logic.
        - Checks if passwords match.
        - Checks if the email is already registered.
        """

        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists!"})

        return attrs

    def create(self, validated_data):
        """
        Overriding the create method to handle password hashing 
        via the custom UserManager.
        """
        # Remove the repeated password before passing data to create_user
        validated_data.pop('repeated_password')

        # Create user using the manager to ensure correct hashing
        user = User.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )
        return user
    

class CustomAuthTokenSerializer(serializers.Serializer):

    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs