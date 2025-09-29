from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import CustomTokenObtainPairSerializer
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserCreateSerializer, UserRoleUpdateSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": getattr(user, "role", "N/A")
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


class OperatorLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None and getattr(user, "role", "").upper() == "OPERADOR":
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Este usuario no es un Operador o las credenciales son inválidas"},
                        status=status.HTTP_401_UNAUTHORIZED)
    
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRoleUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
