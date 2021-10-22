from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def backup_object(instance, target_model, user_id):
    data = {
        field.attname: getattr(instance, field.attname)
        for field in instance._meta.fields if hasattr(target_model, field.attname)
    }
    data['remove_at'] = timezone.now()
    data['remove_id'] = user_id
    target_model.objects.create(**data)


def extended_exception_handler(exc, content):
    if isinstance(exc, ValidationError):
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)
