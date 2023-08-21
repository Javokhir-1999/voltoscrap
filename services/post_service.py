import json

from fastapi import HTTPException
from starlette import status
from tortoise.expressions import Q
from tortoise import Tortoise
import dto
from domain import models
from domain.database_models.enums import AnalizeStatus
from utils.helpers import paginate
import asyncpg

class PostService:
    @classmethod
    def __get_post_dto(cls, instance: models.Post) -> dto.PostDTO:
        return dto.PostDTO(
            id=str(instance.id),
            search_id=str(instance.search_id),
            source=instance.source.value if instance.source else None,
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
    async def get_keyword_by_tone(cls, tone: str):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
            select json_agg(json_build_object('word',p.word,'count', p.count,'comments_count', p.comments_count,'total_count', c.count))
            FROM (
             select word, count(*) as count, sum(comments_count) as comments_count from post where tone='{tone}'  group by word) as p
            JOIN (  
             select word, count(*) as count from post  group by word)
            AS c ON p.word = c.word;
            """)
            data = json.loads(res[1][0][0])
            return {'data':data}
        except Exception as e:
            print("Exception:",e)
    @classmethod
    async def get_source_by_tone(cls, tone: str):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
            select json_agg(json_build_object('author_id',p.author_id,'count', p.count,'comments_count', p.comments_count,'total_count', c.count))
            FROM (
             select author_id, count(*) as count, sum(comments_count) as comments_count from post where tone='{tone}'  group by author_id) as p
            JOIN (  
             select author_id, count(*) as count from post  group by author_id)
            AS c ON p.author_id = c.author_id;
            """)
            data = json.loads(res[1][0][0])
            return {'data':data}
        except Exception as e:
            print("Exception:",e)

    @classmethod
    async def get_tones(cls):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
            select json_build_object('tone',p.tone,'count', p.count)
            FROM  (  
             select tone, count(*) as count from post  group by tone
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
    async def get_tone_by_word(cls,word:str):
        try:
            res = await Tortoise.get_connection('default').execute_query(f"""
            select json_build_object('tone',p.tone,'count', p.count)
            FROM  (  
             select tone, count(*) as count from post where word='{word}' group by tone
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
             select word, count(*) as count from post  group by word
             ) as p
            """)
            tones = []
            d:dict = {}
            for r in res[1]:
                t = json.loads(r[0])
                tones.append({'text':t['word'],'value':t['count']})
            return {'data':tones}
        except Exception as e:
            print("Exception:",e)


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
                post.status = AnalizeStatus[post_input.status.upper()]
            if post_input.word:
                post.word =post_input.word
            if post_input.tone:
                post.tone =post_input.tone
            if post_input.summary:
                post.summary =post_input.summary
            if post_input.text_translated:
                post.text_translated =post_input.text_translated
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
