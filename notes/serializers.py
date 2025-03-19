from rest_framework import serializers
from notes.models import Note
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['url', 'title', 'note', 'created_at', 'last_edited', 'owner']
        lookup_field = 'id'
        extra_kwargs = {
            'owner': {
                'lookup_field': 'id', 
                'view_name': 'user-detail',
                'read_only': True
            }
        }
