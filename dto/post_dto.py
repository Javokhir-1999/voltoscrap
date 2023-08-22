from pydantic import BaseModel, Field

# Data Transfer Object
from dto.base_dto import BaseListDTO


class PostDTO(BaseModel):
    id:str
    search_id:str
    text:str = None
    source:str = None
    url:str = None
    media:list[str] = None
    date:str = None
    top_three_emoji:list[str] = None
    shares:int = 0
    comments_count:int = 0
    status:str
    tone:str = None
    summary:str = None
    text_translated:str = None



class PostInputDTO(BaseModel):
    status:str
    tone:str = None
    word:str = None
    summary:str = None
    text_translated:str = None

class PostWordInputDTO(BaseModel):
    word:str = None


class PostListDTO(BaseListDTO):
    data: list[PostDTO] = []
