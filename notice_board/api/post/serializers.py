from rest_framework import serializers, exceptions

from apps.post.models import Post
from apps.users.models import User


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=2000)

    class Meta:
        model = Post
        fields = ['title', 'content', 'writer']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)
        if instance:
            self.fields.pop('writer')

    def validate(self, attrs):
        if not self.instance:
            writer = attrs.get('writer')
            if writer is None:
                raise exceptions.ValidationError("Must in writer")

            if User.objects.filter(id=writer.id).exists() is False:
                raise exceptions.ValidationError("Not enrollment user")

        return attrs

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }
