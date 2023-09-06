import json

from fastapi import HTTPException
from starlette import status
from tortoise import Tortoise
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
                comment.status = AnalizeStatus[comment_input.status.upper()]
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

    @classmethod
    async def get_tones(cls):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
                select json_build_object('tone',p.tone,'count', p.count)
                FROM  (  
                 select tone, count(*) as count from comment  group by tone
                 ) as p
                """)
            tones = []
            for r in res[1]:
                tones.append(json.loads(r[0]))
            return {'data': tones}
        except Exception as e:
            print("Exception:", e)

    @classmethod
    async def get_tone_by_word(cls,word:str):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
            select json_build_object('tone',p.tone,'count', p.count)
            FROM  (  
             select tone, count(*) as count from comment where word='{word.replace("'","''")}' group by tone
             ) as p
            """)
            tones = []
            print(len(res[1]))
            for r in res[1]:
                tones.append(json.loads(r[0]))
            return {'data':tones}
        except Exception as e:
            print("Exception:",e)

    @classmethod
    async def get_topics(cls):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
                select json_build_object('word',p.word,'count', p.count)
                FROM  (  
                 select word, count(*) as count from comment  group by word
                 ) as p
                """)
            tones = []
            d: dict = {}
            for r in res[1]:
                t = json.loads(r[0])
                tones.append({'text': t['word'], 'value': t['count']})
            return {'data': tones}
        except Exception as e:
            print("Exception:", e)

    @classmethod
    async def get_post_comments_by_tone(cls, tone: str):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
                SELECT json_agg(json_build_object(
                    'post_id', tc.post_id,
                    'post_url', tc.post_url,
                    'tone_comments_count', tc.tcc,
                    'comments_count', c.cc
                )) AS result
                FROM (
                    SELECT p.id AS post_id, p.url AS post_url, COUNT(c.id) AS tcc
                    FROM post p
                    LEFT JOIN comment c ON p.id = c.post_id
                    WHERE c.tone = '{tone}'
                    GROUP BY p.id, p.url
                ) AS tc
                JOIN (
                    SELECT p.id AS post_id, COUNT(c.id) AS cc
                    FROM post p
                    LEFT JOIN comment c ON p.id = c.post_id
                    GROUP BY p.id
                ) AS c ON tc.post_id = c.post_id;
                """)
            data = json.loads(res[1][0][0])
            return {'data': data}
        except Exception as e:
            print("Exception:", e)