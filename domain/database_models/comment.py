import uuid
from tortoise import fields
from tortoise.models import Model
from domain.database_models.enums import AnalizeStatus, Source

from domain.database_models.base import BaseDBModel


class Comment(Model,BaseDBModel):
    post = fields.ForeignKeyField(
        "models.Post",
        on_delete=fields.SET_NULL,
        null=True,
        related_name='comments'
    )
    search = fields.ForeignKeyField(
        "models.Search",
        on_delete=fields.SET_NULL,
        null=True,
        related_name='comments'
    )
    reply_comment = fields.ForeignKeyField(
        "models.Comment",
        on_delete=fields.SET_NULL,
        null=True,
        related_name='replies'
    )
    comment_source_unique_id = fields.CharField(unique=True, max_length=200, null=True)
    reply_url = fields.CharField(max_length=500,null=True)
    post_source_id = fields.CharField(max_length=200,null=True)
    source = fields.CharEnumField(enum_type=Source, null=True)
    author = fields.CharField(max_length=50)
    author_id = fields.CharField(max_length=50)
    text = fields.TextField(null=True)
    url = fields.CharField(max_length=1000)
    media = fields.JSONField(null=True)
    date = fields.DatetimeField(null=True)
    emoji = fields.JSONField(null=True)
    top_three_emoji = fields.JSONField(null=True)
    status = fields.CharEnumField(enum_type=AnalizeStatus)
    tone = fields.CharField(max_length=100, null=True)#
    summary = fields.CharField(max_length=500, null=True)#
    data = fields.JSONField(null=True)
    post_id:uuid.UUID
    search_id:uuid.UUID
    class Meta:
        indexes = [('post_id',),]