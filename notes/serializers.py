from rest_framework import serializers
from notes.models import Note, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    tag_list = serializers.StringRelatedField(source='tags', many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['url', 'title', 'note', 'created_at', 'last_edited', 'owner', 'tags', 'tag_list']
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
            }
        }

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        note = super().update(instance, validated_data)
        
        if tags_data:
            # Clear existing tags if new ones are provided
            note.tags.clear()
            if tags_data != ["clear"]:
                for tag_name in tags_data:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    note.tags.add(tag)
        
        return note

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        note = super().create(validated_data)
        
        # Create or get existing tags and add them to the note
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            note.tags.add(tag)
        
        return note

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