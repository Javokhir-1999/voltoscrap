from fastapi import APIRouter

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


@router.put("/put/{id}", response_model=dto.PostDTO)
async def update_post(id: str, post_input: dto.PostInputDTO) -> ModelResponse:
    post: dto.PostDTO = await services.PostService.update_data(post_id=id, post_input=post_input)
    return ModelResponse(
        dto_model=post
    )


@router.get('/list/')
async def get_post_list(search_id:str=None, page: int = 1, page_size: int = 10) -> ModelResponse:
    posts: dto.PostListDTO = await services.PostService.get_list(search_id=search_id,page=page, page_size=page_size)
    return ModelResponse(
        dto_model=posts
    )


@router.delete('/delete/{id}')
async def delete_post(id: str) -> ModelResponse:
    delete_msg: dto.DeleteMsgDTO = await services.PostService.delete_data(post_id=id)
    return ModelResponse(
        dto_model=delete_msg
    )
