from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

from users.models import User
from .serializers import CustomAuthTokenSerializer, RegistrationSerializer


class LoginView(ObtainAuthToken):
    """
    API View to handle user login.
    Uses a custom serializer to validate email and password, then returns a token.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        """Initialize the serializer with request data and context"""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            """Retrieve the authenticated user from the serializer"""
            user = serializer.validated_data['user']
            """Get an existing token or create a new one for the user"""
            token, created = Token.objects.get_or_create(user=user)
            
            """Return token and user profile information"""
            return Response({
                "token": token.key,
                "fullname": user.fullname,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_200_OK)
            
        """Return validation errors if authentication fails"""
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegistrationView(APIView):
    """
    API View to handle new user registration.
    Validates input data, creates a user, and returns an auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            """Initialize the registration serializer with input data"""
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                """Save the new user to the database"""
                saved_account = serializer.save()
                """Generate a token for the newly registered user"""
                token, created = Token.objects.get_or_create(user=saved_account)
                
                """Return 201 Created with user details and token"""
                return Response({
                    "token": token.key,
                    "fullname": saved_account.fullname,
                    "email": saved_account.email,
                    "user_id": saved_account.id
                }, status=status.HTTP_201_CREATED)
            else:
                """Return 400 Bad Request if the input data is invalid"""
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            """General exception handling for server-side errors"""
            return ResponseResponse(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmailCheckView(APIView):
    """
    API View to check if a user with a specific email exists.
    Useful for member search and validation in board tasks.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get the email from the URL query parameters"""
        email = request.query_params.get('email')
        
        """Ensure the email parameter is provided in the request"""
        if not email:
            return Response(
                {"detail": "Email field is missing."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            """Attempt to find the user by their unique email"""
            user = User.objects.get(email=email)
            return Response({
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            """Return 404 if no user is found with the provided email"""
            return Response(
                {"detail": "Email not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )