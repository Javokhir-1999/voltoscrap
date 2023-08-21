import uuid
from tortoise import fields
from tortoise.models import Model
from domain.database_models.enums import AnalizeStatus

from domain.database_models.base import BaseDBModel


class Comment(Model,BaseDBModel):
    post = fields.ForeignKeyField(
        "models.Post",
        on_delete=fields.SET_NULL,
        null=True,
        related_name='comments'
    )
    author = fields.CharField(max_length=50)
    text = fields.TextField(null=True)
    url = fields.CharField(max_length=1000)
    media = fields.JSONField(null=True)
    date = fields.DatetimeField(null=True)
    status = fields.CharEnumField(enum_type=AnalizeStatus)
    data = fields.JSONField(null=True)
    post_id:uuid.UUID
    class Meta:
        indexes = [('post_id',),]