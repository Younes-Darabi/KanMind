from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation and password confirmation logic.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        """
        Validate that the two passwords match and the email is unique.
        """
        """Check if the password and confirmation password are identical"""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})
        
        """Ensure the email address is not already registered in the system"""
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists!"})
        
        return attrs

    def create(self, validated_data):
        """
        Create and return a new User instance using the custom UserManager.
        """
        """Remove the repeated_password as it's not a field in the User model"""
        validated_data.pop('repeated_password')
        
        """Use the create_user method to handle password hashing"""
        user = User.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )
        return user
    

class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user authentication.
    Validates the provided email and password and returns an authenticated user.
    """
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Authenticate the user using the provided credentials.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            """Use Django's authenticate method (passing email as the username)"""
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            
            """If authentication fails, raise a validation error"""
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            """Ensure both fields are present in the request"""
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        """Attach the authenticated user object to the validated data"""
        attrs['user'] = user
        return attrs