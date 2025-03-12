from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from notes.models import Note
from django.contrib.auth import get_user_model
from notes.serializers import NoteSerializer

User = get_user_model()


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NotesSpecificUser(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
