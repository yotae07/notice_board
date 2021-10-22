from rest_framework import mixins, permissions, exceptions
from rest_framework.viewsets import GenericViewSet

from api.post.serializers import PostSerializer
from api.utils import backup_object
from apps.post.models import Post, DeletePost


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]

        return super().get_permissions()

    def get_object(self):
        instance = super().get_object()
        if self.action in ['partial_update', 'destroy'] and self.request.user != instance.writer:
            raise exceptions.ValidationError("Can't approach other user post")

        return instance

    def perform_destroy(self, instance):
        backup_object(instance, DeletePost, self.request.user.id)
        super().perform_destroy(instance)
