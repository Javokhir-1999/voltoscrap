from pydantic import BaseModel
from dto import BaseListDTO





class OrderDebtDTO(BaseModel):
    id: str
    created_at:str
    user_id: str = None
    user_full_name: str = None
    phone_number:str = None
    payment_type: str = None
    payment_status: str = None
    items_count:int = 0
    amount:float = 0
    paid:float = 0


class OrderDebtListDTO(BaseListDTO):
    data: list[OrderDebtDTO] = []


