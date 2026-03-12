from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        email = self.validated_data['email']
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        user_email = self.validated_data['email']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match!'})

        if User.objects.filter(email=user_email).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
            
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'Username already exists!'})
    
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        account.set_password(pw)
        account.save()
        return account