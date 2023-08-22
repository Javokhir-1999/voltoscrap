from fastapi import APIRouter

import dto
import services
from utils.responses.model_response import ModelResponse

router = APIRouter()


@router.get("/get/{id}", response_model=dto.CommentDTO)
async def get_comment(id: str) -> ModelResponse:
    comment: dto.CommentDTO = await services.CommentService.get_detail(comment_id=id)
    return ModelResponse(
        dto_model=comment
    )


@router.put("/put/{id}", response_model=dto.CommentDTO)
async def update_comment(id: str, comment_input: dto.CommentInputDTO) -> ModelResponse:
    comment: dto.CommentDTO = await services.CommentService.update_data(comment_id=id, comment_input=comment_input)
    return ModelResponse(
        dto_model=comment
    )


@router.get('/list/')
async def comment_list(post_id:str = None,page: int = 1, page_size: int = 10) -> ModelResponse:
    comments: dto.CommentListDTO = await services.CommentService.get_list(post_id=post_id,page=page, page_size=page_size)
    return ModelResponse(
        dto_model=comments
    )


@router.delete('/delete/{id}')
async def delete_comment(id: str) -> ModelResponse:
    delete_msg: dto.DeleteMsgDTO = await services.CommentService.delete_data(comment_id=id)
    return ModelResponse(
        dto_model=delete_msg
    )
