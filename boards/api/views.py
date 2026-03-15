from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from boards.api.permissions import IsOwnerOrReadOnly
from boards.models import Board
from .serializers import BoardSerializer

class BoardListCreateView(generics.ListCreateAPIView):

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]