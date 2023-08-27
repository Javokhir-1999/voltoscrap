from fastapi import HTTPException
from starlette import status
from tortoise.expressions import Q

import dto
from domain import models
from domain.database_models.enums import SearchStatus
from utils.helpers import paginate


class SearchService:
    @classmethod
    def __get_search_dto(cls, instance: models.Search) -> dto.SearchDTO:
        return dto.SearchDTO(
            id=str(instance.id),
            words=instance.word,
            posts=instance.post,
            use_telegram=instance.use_telegram,
            telegram_limit=instance.telegram_limit,
            telegram_channels=instance.telegram_channel,
            use_facebook=instance.use_facebook,
            facebook_limit=instance.facebook_limit,
            facebook_channels=instance.facebook_channel,
            status=instance.status.value
        )

    @classmethod
    async def get_detail(cls, search_id: str) -> dto.SearchDTO:
        search: models.Search = await models.Search.get_or_none(id=search_id)
        if search:
            return cls.__get_search_dto(search)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Search not found")

    @classmethod
    async def add_data(cls, search_input: dto.SearchInputDTO) -> dto.SearchDTO:
        search: models.Search = await models.Search.create(
            word=','.join(search_input.words).replace("`","'"),
            post=','.join(search_input.posts) if search_input.posts else None,
            use_telegram=search_input.use_telegram,
            telegram_limit=search_input.telegram_limit,
            telegram_channel=','.join(search_input.telegram_channels) if search_input.telegram_channels else None,
            use_facebook=search_input.use_facebook,
            facebook_limit=search_input.facebook_limit,
            facebook_channel=','.join(search_input.facebook_channels) if search_input.facebook_channels else None,
            status=SearchStatus.NEW
        )
        return cls.__get_search_dto(search)

    @classmethod
    async def get_list(cls,search_text:str = None, page: int = 1, page_size: int = 10) -> dto.SearchListDTO:
        query = Q()
        if search_text:
            query = query & Q(word=search_text)
        searchs, total = await paginate(
            models.Search.filter(query),
            page_size=page_size,
            page=page,
            prefetch_related=True
        )
        return dto.SearchListDTO(
            data=[cls.__get_search_dto(search) for search in searchs],
            page=page,
            page_size=page_size,
            total=total
        )

    @classmethod
    async def delete_data(cls, search_id: str) -> dto.DeleteMsgDTO:
        search: models.Search | None = await models.Search.get_or_none(id=search_id)
        if search is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Search {search_id} not found")
        await search.delete()
        return dto.DeleteMsgDTO(msg=f"Search {search_id} successfully deleted")
