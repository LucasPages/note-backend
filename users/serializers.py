from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'notes']
        lookup_field = 'id'

        extra_kwargs = {
            'url': {
                'lookup_field': 'id',
                'view_name': 'user-detail'
            },
            'notes': {
                'lookup_field': 'id',
                'view_name': 'note-detail',
                'read_only': True,
                'many': True
            }
        }
