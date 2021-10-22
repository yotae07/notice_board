from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from api.signup.serializers import SignupSerializer
from apps.users.models import User


class SignupViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]
