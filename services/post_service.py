from fastapi import HTTPException
from starlette import status
from tortoise.expressions import Q

import dto
from domain import models
from domain.database_models.enums import AnalizeStatus
from utils.helpers import paginate


class PostService:
    @classmethod
    def __get_post_dto(cls, instance: models.Post) -> dto.PostDTO:
        return dto.PostDTO(
            id=str(instance.id),
            search_id=str(instance.search_id),
            author=instance.author,
            text=instance.text,
            url=instance.url,
            date=str(instance.date),
            shares=instance.shares,
            comments_count=instance.comments_count,
            status=instance.status.value,
            tone=instance.tone,
            summary=instance.summary
        )

    @classmethod
    async def get_detail(cls, post_id: str) -> dto.PostDTO:
        post: models.Post = await models.Post.get_or_none(id=post_id)
        if post:
            return cls.__get_post_dto(post)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")

    @classmethod
    async def get_list(cls,search_id:str = None, page: int = 1, page_size: int = 10) -> dto.PostListDTO:
        query = Q()
        if search_id:
            query = query & Q(search_id=search_id)
        posts, total = await paginate(
            models.Post.filter(query),
            page_size=page_size,
            page=page,
            prefetch_related=True
        )
        return dto.PostListDTO(
            data=[cls.__get_post_dto(post) for post in posts],
            page=page,
            page_size=page_size,
            total=total
        )

    @classmethod
    async def update_data(cls, post_id: str, post_input: dto.PostInputDTO) -> dto.PostDTO:
        post: models.Post = await models.Post.get_or_none(id=post_id)
        if post:
            if post_input.status:
                post.status = AnalizeStatus[post_input.status]
            if post_input.tone:
                post.tone =post_input.tone
            if post_input.summary:
                post.summary =post_input.summary
            await post.save()
            return cls.__get_post_dto(post)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")


    @classmethod
    async def delete_data(cls, post_id: str) -> dto.DeleteMsgDTO:
        post: models.Post | None = await models.Post.get_or_none(id=post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
        await post.delete()
        return dto.DeleteMsgDTO(msg=f"Post {post_id} successfully deleted")
