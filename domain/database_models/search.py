from tortoise import fields
from tortoise.expressions import Q
from tortoise.models import Model
from domain.database_models.enums import SearchStatus, Source

from domain.database_models.base import BaseDBModel



class Search(Model,BaseDBModel):
    word = fields.TextField(null=True)
    fb_post = fields.TextField(null=True)
    use_telegram = fields.BooleanField(null=True, default=False)
    telegram_limit = fields.IntField(null=True, ge=1,default=5)
    telegram_channel = fields.CharField(null=True, min_length=3, max_length=2000, default=None)
    use_facebook = fields.BooleanField(null=True, default=False)
    facebook_limit = fields.IntField(null=True, ge=2,default=10)
    facebook_channel = fields.CharField(null=True, min_length=3, max_length=2000, default=None)
    status = fields.CharEnumField(enum_type=SearchStatus)
    tg_posts_count = fields.IntField(null=True, default=0)
    tg_comments_count = fields.IntField(null=True, default=0)
    fb_posts_count = fields.IntField(null=True, default=0)
    fb_comments_count = fields.IntField(null=True, default=0)
    async def recalc_counts(self):
        from domain.database_models.post import Post
        from domain.database_models.comment import Comment
        self.tg_posts_count = await Post.filter(Q(search_id=self.id) & Q(source=Source.TG)).count()
        self.tg_comments_count = await Comment.filter(Q(search_id=self.id) & Q(source=Source.TG)).count()
        self.fb_posts_count = await Post.filter(Q(search_id=self.id) & Q(source=Source.FB)).count()
        self.fb_comments_count = await Comment.filter(Q(search_id=self.id) & Q(source=Source.FB)).count()
        await self.save()