from pydantic import BaseModel

class CreateTeamDTO(BaseModel):
    customer_name : str
    product_code : str
    total_amount : float
    status: str