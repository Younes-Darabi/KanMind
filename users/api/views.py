from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer


class RegistrationView(generics.CreateAPIView):

    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "fullname": user.fullname,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
