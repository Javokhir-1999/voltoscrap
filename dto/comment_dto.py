from pydantic import BaseModel, Field

# Data Transfer Object
from dto.base_dto import BaseListDTO

class CommentDTO(BaseModel):
    id:str
    post_id:str
    author:str = None
    text:str = None
    url:str = None
    media:list[str] = None
    date:str = None
    status:str
    tone:str = None
    summary:str = None



class CommentInputDTO(BaseModel):
    status:str
    tone:str = None
    summary:str = None


class CommentListDTO(BaseListDTO):
    data: list[CommentDTO] = []
