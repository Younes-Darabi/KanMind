from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "fullname": user.fullname,
                    "email": user.email,
                    "user_id": user.id
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                saved_account = serializer.save()
                token, created = Token.objects.get_or_create(user=saved_account)
                return Response({
                    "token": token.key,
                    "fullname": saved_account.fullname,
                    "email": saved_account.email,
                    "user_id": saved_account.id
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )