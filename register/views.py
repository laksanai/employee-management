from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]