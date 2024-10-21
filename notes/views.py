from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from notes.permissions import IsAuthorOfNote, IsUser
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from notes.models import Note
from django.contrib.auth.models import User
from notes.serializers import NoteSerializer, UserSerializer


class NoteViewSet(viewsets.ModelViewSet):
    # TODO: Remove capacity of superuser to look at user notes (change permission) (useful for development)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthorOfNote]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    # TODO: Make it so that the admin user cannot see the notes field of a user (except for his)
    #       this could be done with different serializer classes (Admin vs User) with hidden fields ?
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser]


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class NotesSpecificUser(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
