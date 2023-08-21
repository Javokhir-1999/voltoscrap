from fastapi import APIRouter, BackgroundTasks

import dto
import services
from utils.responses.model_response import ModelResponse
from scripts.tg.start import get_channel_messages

router = APIRouter()


@router.get("/get/{id}", response_model=dto.SearchDTO)
async def get_search(id: str) -> ModelResponse:
    search: dto.SearchDTO = await services.SearchService.get_detail(search_id=id)
    return ModelResponse(
        dto_model=search
    )


@router.post("/post/", response_model=dto.SearchDTO)
async def post_search(search_input: dto.SearchInputDTO, background_tasks: BackgroundTasks) -> ModelResponse:
    search: dto.SearchDTO = await services.SearchService.add_data(search_input=search_input)
    
    if search.use_telegram:
        background_tasks.add_task(get_channel_messages, search)
    
    return ModelResponse(
        dto_model=search
    )


@router.get('/list/')
async def get_search_list(search_text: str = None, page: int = 1, page_size: int = 10) -> ModelResponse:
    searchs: dto.SearchListDTO = await services.SearchService.get_list(search_text=search_text,page=page, page_size=page_size)
    return ModelResponse(
        dto_model=searchs
    )


@router.delete('/delete/{id}')
async def delete_search(id: str) -> ModelResponse:
    delete_msg: dto.DeleteMsgDTO = await services.SearchService.delete_data(search_id=id)
    return ModelResponse(
        dto_model=delete_msg
    )
