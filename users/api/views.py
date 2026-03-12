from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            full_name = saved_account.get_full_name()
            data = {
                'token': token.key,
                'fullname': saved_account.full_name,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response(data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
class LoginView(APIView):
    pass