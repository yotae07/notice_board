from django.db import models

from apps.users.models import User
from ..models import BaseModel


class AbstractPost(BaseModel):
    title = models.CharField(max_length=50)
    content = models.TextField()
    writer = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name='writer',
        db_constraint=False,
        db_index=True
    )

    class Meta:
        abstract = True


class Post(AbstractPost):
    class Meta:
        verbose_name = 'post'

    def __str__(self):
        return f"{self.id} {self.title}"


class DeletePost(AbstractPost):
    remove_id = models.BigIntegerField()
    remove_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'delete_post'

    def __str__(self):
        return f"{self.id} {self.title} {self.remove_id}"
