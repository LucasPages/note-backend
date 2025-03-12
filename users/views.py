from rest_framework import viewsets
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

