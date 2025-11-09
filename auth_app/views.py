from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .serializers import RegisterSerializer
from rest_framework.response import Response

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LogoutView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "logged out"})