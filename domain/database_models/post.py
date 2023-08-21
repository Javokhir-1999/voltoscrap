import uuid
from tortoise import fields
from tortoise.models import Model
from domain.database_models.enums import AnalizeStatus, Source
from domain.database_models.base import BaseDBModel


class Post(Model,BaseDBModel):
    search = fields.ForeignKeyField(
        "models.Search",
        on_delete=fields.SET_NULL,
        null=True,
        related_name='posts'
    )
    pos_source_unique_id = fields.CharField(unique=True, max_length=20, null=True)
    source = fields.CharEnumField(enum_type=Source, null=True)
    author = fields.CharField(max_length=50, null=True)
    author_id = fields.CharField(max_length=50,null=True)
    text = fields.TextField(null=True)
    url = fields.CharField(max_length=1000, null=True)
    media = fields.JSONField(null=True)
    date = fields.DatetimeField(null=True)
    emoji = fields.JSONField(null=True)
    top_three_emoji = fields.JSONField(null=True)
    shares = fields.IntField(null=True, default=0)
    comments_count = fields.IntField(null=True, default=0)
    status = fields.CharEnumField(enum_type=AnalizeStatus)#
    data = fields.JSONField(null=True)
    tone = fields.CharField(max_length=100, null=True)#
    summary = fields.CharField(max_length=500, null=True)#
    search_id:uuid.UUID
    comments: fields.ReverseRelation["models.Comment"]

    class Meta:
        indexes = [('search_id',),]

