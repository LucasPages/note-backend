from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
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
