from rest_framework import serializers
from notes.models import Note
from django.contrib.auth.models import User


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    notes = serializers.HyperlinkedRelatedField(view_name="note-detail", required=False, many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ['url','email', 'username', 'password', 'notes']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User(email=validated_data["email"],
                    username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
