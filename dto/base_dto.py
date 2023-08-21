from pydantic import BaseModel



class BaseListDTO(BaseModel):
    page:int = 1
    page_size:int = 10
    total:int = 0


class DeleteMsgDTO(BaseModel):
    msg:str = "Successfully deleted"

class NotFoundMsgDTO(BaseModel):
    msg:str = "Not found"

class ErrorMsgDTO(BaseModel):
    msg:str = "Some error!"

class InfoMsgDTO(BaseModel):
    msg:str = "Done!"