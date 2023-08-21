from tortoise import fields


class BaseDBModel:
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    description = fields.CharField(max_length=255,null=True)