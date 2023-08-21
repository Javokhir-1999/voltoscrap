from tortoise import fields
from tortoise.models import Model

from domain.database_models.base import BaseDBModel


class Category(Model,BaseDBModel):
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=500,null=True)
    image2 = fields.CharField(max_length=500,null=True)
    parent = fields.ForeignKeyField(
        "models.Category",
        on_delete=fields.SET_NULL,
        null=True,
        related_name='sub_categories',
        none=True,
    )

    class Meta:
        indexes = [('author',),('author', 'parent')]