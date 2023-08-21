from fastapi import HTTPException
from starlette import status
from tortoise.expressions import Q

import dto
from domain import models
from domain.database_models.enums import AnalizeStatus
from utils.helpers import paginate


class CommentService:
    @classmethod
    def __get_comment_dto(cls, instance: models.Comment) -> dto.CommentDTO:
        return dto.CommentDTO(
            id=str(instance.id),
            post_id=str(instance.post_id),
            author=instance.author,
            text=instance.text,
            url=instance.url,
            date=str(instance.date),
            status=instance.status.value,
            tone=instance.tone,
            summary=instance.summary
        )

    @classmethod
    async def get_detail(cls, comment_id: str) -> dto.CommentDTO:
        comment: models.Comment = await models.Comment.get_or_none(id=comment_id)
        if comment:
            return cls.__get_comment_dto(comment)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment not found")

    @classmethod
    async def get_list(cls,post_id:str = None, page: int = 1, page_size: int = 10) -> dto.CommentListDTO:
        query = Q()
        if post_id:
            query = query & Q(post_id=post_id)
        comments, total = await paginate(
            models.Comment.filter(query),
            page_size=page_size,
            page=page,
            prefetch_related=True
        )
        return dto.CommentListDTO(
            data=[cls.__get_comment_dto(comment) for comment in comments],
            page=page,
            page_size=page_size,
            total=total
        )

    @classmethod
    async def update_data(cls, comment_id: str, comment_input: dto.CommentInputDTO) -> dto.CommentDTO:
        comment: models.Comment = await models.Comment.get_or_none(id=comment_id)
        if comment:
            if comment_input.status:
                comment.status = AnalizeStatus[comment_input.status]
            if comment_input.tone:
                comment.tone =comment_input.tone
            if comment_input.summary:
                comment.summary =comment_input.summary
            await comment.save()
            return cls.__get_comment_dto(comment)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")


    @classmethod
    async def delete_data(cls, comment_id: str) -> dto.DeleteMsgDTO:
        comment: models.Comment | None = await models.Comment.get_or_none(id=comment_id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")
        await comment.delete()
        return dto.DeleteMsgDTO(msg=f"Comment {comment_id} successfully deleted")
