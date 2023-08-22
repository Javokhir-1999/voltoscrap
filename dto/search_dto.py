from pydantic import BaseModel, Field

# Data Transfer Object
from dto.base_dto import BaseListDTO


class SearchDTO(BaseModel):
    id: str
    words: str
    telegram_channels: str = Field(min_length=3, default=None)
    use_telegram: bool =  False
    telegram_limit:int = Field(ge=1,default=5)
    use_facebook: bool =  False
    facebook_limit:int = Field(ge=2,default=10)
    facebook_channels: str = None
    status:str



class SearchInputDTO(BaseModel):
    words: list[str]
    use_telegram: bool =  False
    telegram_limit:int = Field(ge=1,default=5)
    telegram_channels:list[str] = None
    use_facebook: bool =  False
    facebook_limit:int = Field(ge=2,default=10)
    facebook_channels:list[str] = None


class SearchListDTO(BaseListDTO):
    data: list[SearchDTO] = []
