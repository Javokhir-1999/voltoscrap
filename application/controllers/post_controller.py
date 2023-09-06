from fastapi import APIRouter
from starlette.responses import JSONResponse

import dto
import services
from utils.responses.model_response import ModelResponse

router = APIRouter()


@router.get("/get/{id}", response_model=dto.PostDTO)
async def get_post(id: str) -> ModelResponse:
    post: dto.PostDTO = await services.PostService.get_detail(post_id=id)
    return ModelResponse(
        dto_model=post
    )


@router.get("/get-stat-by-tone/", response_model=dto.PostDTO)
async def get_stat_by_tone(tone: str, search_id:str=None):
    data: dict = await services.PostService.get_keyword_by_tone(tone=tone,search_id=search_id)
    return JSONResponse(
        content=data
    )


@router.get("/get-source-by-tone/", response_model=dto.PostDTO)
async def get_source_by_tone(tone: str, search_id:str=None):
    data: dict = await services.PostService.get_source_by_tone(tone=tone,search_id=search_id)
    return JSONResponse(
        content=data
    )


@router.get("/get-tones/", response_model=dto.PostDTO)
async def get_tones(search_id:str=None):
    data: dict = await services.PostService.get_tones(search_id=search_id)
    return JSONResponse(
        content=data
    )


@router.post("/get-tone-by-word/", response_model=dto.PostDTO)
async def get_tone_by_word(word_input: dto.PostWordInputDTO, search_id:str=None):
    data: dict = await services.PostService.get_tone_by_word(word=word_input.word, search_id=search_id)
    return JSONResponse(
        content=data
    )


@router.get("/get-topics/", response_model=dto.PostDTO)
async def get_topics(search_id:str=None):
    data: dict = await services.PostService.get_topics(search_id=search_id)
    return JSONResponse(
        content=data
    )


@router.put("/put/{id}", response_model=dto.PostDTO)
async def update_post(id: str, post_input: dto.PostInputDTO):
    post: dto.PostDTO = await services.PostService.update_data(post_id=id, post_input=post_input)
    return ModelResponse(
        dto_model=post
    )


@router.get('/list/')
async def get_post_list(search_id: str = None,status:str = None, page: int = 1, page_size: int = 10) -> ModelResponse:
    posts: dto.PostListDTO = await services.PostService.get_list(search_id=search_id,status=status, page=page, page_size=page_size)
    return ModelResponse(
        dto_model=posts
    )


@router.delete('/delete/{id}')
async def delete_post(id: str) -> ModelResponse:
    delete_msg: dto.DeleteMsgDTO = await services.PostService.delete_data(post_id=id)
    return ModelResponse(
        dto_model=delete_msg
    )
