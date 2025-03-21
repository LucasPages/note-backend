from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    title = models.TextField(max_length=20, blank=True)
    note = models.TextField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if len(self.note) > 20:
            string = self.note[:20] + "..."
        else:
            string = self.note
        return f"{self.title} : {string}"


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    notes = models.ManyToManyField(Note, related_name='tags')

    def __str__(self) -> str:
        return self.name
