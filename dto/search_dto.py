from pydantic import BaseModel, Field

# Data Transfer Object
from dto.base_dto import BaseListDTO


class SearchDTO(BaseModel):
    id: str
    words: str
    fb_posts: str = None
    telegram_channels: str = Field(min_length=3, default=None)
    use_telegram: bool =  False
    telegram_limit:int = Field(ge=1,default=5)
    use_facebook: bool =  False
    facebook_limit:int = Field(ge=2,default=10)
    facebook_channels: str = None
    status:str
    tg_posts_count:int = None
    tg_comments_count:int = None
    fb_posts_count:int = None
    fb_comments_count:int = None



class SearchInputDTO(BaseModel):
    words: list[str]
    fb_posts: list[str] = None
    use_telegram: bool =  False
    telegram_limit:int = Field(ge=1,default=5)
    telegram_channels:list[str] = None
    use_facebook: bool =  False
    facebook_limit:int = Field(ge=2,default=10)
    facebook_channels:list[str] = None


class SearchListDTO(BaseListDTO):
    data: list[SearchDTO] = []
