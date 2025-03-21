from rest_framework import serializers
from notes.models import Note, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['url', 'title', 'note', 'created_at', 'last_edited', 'owner', 'tags']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {
                'lookup_field': 'id',
                'view_name': 'note-detail'
            },
            'owner': {
                'lookup_field': 'id', 
                'view_name': 'user-detail',
                'read_only': True
            },
            'tags': {
                'lookup_field': 'id',
                'view_name': 'tag-detail',
                'many': True
            }
        }

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name', 'notes']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {
                'lookup_field': 'id',
                'view_name': 'tag-detail'
            },
            'notes': {
                'lookup_field': 'id',
                'view_name': 'note-detail',
                'read_only': True,
                'many': True
            }
        }