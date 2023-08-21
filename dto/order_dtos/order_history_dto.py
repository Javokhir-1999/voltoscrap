from pydantic import BaseModel

from dto import BaseListDTO
from dto.payment_dto import TotoalPaymentByType

class OrderHistoryItemDTO(BaseModel):
    id:str
    product_id:str
    product_name:str = None
    price:float
    quantity:float
    returned_quantity:float = None
    status:str = None

class OrderHistoryDTO(BaseModel):
    id: str
    created_at: str
    payment_type: str = None
    items_count: int = 0
    amount: float = 0
    paid: float = 0

class OrderHistoryDetailDTO(BaseModel):
    id: str
    created_at: str
    user_id: str = None
    user_full_name: str = None
    payment_type: str = None
    items_count: int = 0
    amount: float = 0
    paid: float = 0
    items: list[OrderHistoryItemDTO] = None


class OrderHistoryListDTO(BaseListDTO):
    payment: TotoalPaymentByType
    data: list[OrderHistoryDTO] = []
