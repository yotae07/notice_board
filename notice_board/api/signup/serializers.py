from django.contrib.auth.hashers import make_password
from django.core import validators
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=5,
        max_length=32,
        validators=[
            validators.RegexValidator(r'^(?!_)[a-zA-Z0-9_.]+$', 'Can use alphabet, digits, _, .'),
            UniqueValidator(queryset=User.objects.all())
        ])
    name = serializers.CharField(
        max_length=30,
        validators=[validators.RegexValidator(r'[\u3130-\u318F\uAC00-\uD7A3]+', 'Can only use korean')]
    )
    email = serializers.EmailField()
    phone = serializers.CharField(
        max_length=20,
        validators=[validators.RegexValidator(r'^[0-9]+$', 'Can only use digits')]
    )
    password = serializers.CharField(min_length=8, max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'role', 'phone', 'email', 'password', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_password(self, value):
        value = make_password(value)
        return value
