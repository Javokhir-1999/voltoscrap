from tortoise import fields
from tortoise.models import Model
from domain.database_models.enums import SearchStatus

from domain.database_models.base import BaseDBModel


class Search(Model,BaseDBModel):
    word = fields.TextField(null=True)
    use_telegram = fields.BooleanField(null=True, default=False)
    telegram_limit = fields.IntField(null=True, ge=1,default=5)
    telegram_channel = fields.CharField(null=True, min_length=3, max_length=100, default=None)
    use_facebook = fields.BooleanField(null=True, default=False)
    facebook_limit = fields.IntField(null=True, ge=2,default=10)
    status = fields.CharEnumField(enum_type=SearchStatus)