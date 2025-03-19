
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from auth.serializers import LoginSerializer

class LoginView(APIView):
    serializer_class = LoginSerializer

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({
            'success': True,
            'message': 'CSRF cookie set'
        })

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({
                'error': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'user': {
                    'email': user.email,
                    'id': str(user.id)
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            'success': True,
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)

