from django.utils import timezone


def backup_object(instance, target_model, user_id):
    data = {
        field.attname: getattr(instance, field.attname)
        for field in instance._meta.fields if hasattr(target_model, field.attname)
    }
    data['remove_at'] = timezone.now()
    data['remove_id'] = user_id
    target_model.objects.create(**data)