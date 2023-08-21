from pydantic import BaseModel, Field

# Data Transfer Object
from dto.base_dto import BaseListDTO


class SearchDTO(BaseModel):
    id: str
    word: str
    telegram_channel: str = Field(min_length=3, default=None)
    use_telegram: bool =  False
    telegram_limit:int = Field(ge=1,default=5)
    use_facebook: bool =  False
    facebook_limit:int = Field(ge=2,default=10)
    status:str



class SearchInputDTO(BaseModel):
    word: str
    use_telegram: bool =  False
    telegram_limit:int = Field(ge=1,default=5)
    telegram_channel:str = Field(min_length=3, default=None)
    use_facebook: bool =  False
    facebook_limit:int = Field(ge=2,default=10)


class SearchListDTO(BaseListDTO):
    data: list[SearchDTO] = []
