from pydantic import BaseModel
from dto.payment_dto import PaymentDTO, PaymentInputInlineDTO
from dto import BaseListDTO



class OrderItemDTO(BaseModel):
    id: str
    product_id: str
    product_name: str = None
    price: float
    quantity: float
    returned_quantity: float = None
    status: str = None

class OrderItemInputDTO(BaseModel):
    product_id:str
    quantity:float

class OrderDTO(BaseModel):
    id: str
    created_at:str
    user_id: str = None
    user_full_name: str = None
    session_id:str = None
    seller_name:str = None
    payment_type: str = None
    payment_status: str = None
    items_count:int = 0
    amount:float = 0
    paid:float = 0
    items:list[OrderItemDTO] = None
    payments:list[PaymentDTO] = None



class OrderInputDTO(BaseModel):
    user_id: str = None
    items:list[OrderItemInputDTO]
    payments:list[PaymentInputInlineDTO]



class OrderListDTO(BaseListDTO):
    data: list[OrderDTO] = []


