from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Optional,Literal
app = FastAPI()

#dữ liệu mẫu
carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]

#model cho carriers
class Carrier(BaseModel):
    code: str
    name: str = Field(min_lengt=3)
    max_weight_capacity: int = Field(gt=0)
    status: Literal["ACTIVE", "INACTIVE", "SUSPENDED"]

class Shipment(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: Literal["MORNING", "AFTERNOON", "NIGHT"]
#hàm thêm 
@app.post("/carriers")
def create_carrier(new_carrier : Carrier):
    for carrier in carriers:
        if carriers["id"] == Carrier.code:
            raise HTTPException(
                status_code=400,
                detail="code không được trùng lặp trong hệ thống"
            )
    #tạo id
    new_id = len(carriers)+1
    new_data ={
        "id":new_id,
        "code":new_carrier.code,
        "name":new_carrier.name,
        "max_weight_capacity":new_carrier.max_weight_capacity,
        "status":new_carrier.status
    }
    carriers.append(new_data)
    return new_data
#lấy full danh sách vận chuyển
@app.get("/carriers")
def get_carriers(
    key_word: Optional[str] =None,
    status: Optional[str]=None,
    min_weight:Optional[int]=None
):
    result=[]
    for carrier in carriers:
        if key_word:
            kw = key_word.lower()
            code_lower = carrier["code"].lower()
            name_lower = carrier["name"].lower()
            if (kw not in code_lower) and (kw not in name_lower):
                continue
        if status:
            if carrier["status"] != status:
                continue
        if min_weight:
            if carrier["max_weight_capacity"] < min_weight:
                continue
        result.append(carrier)
    return result
#lấy chi tiết thông tin
@app.get("/carriers/{carrier_id}")
def get_carrier_id(carrier_id: int):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return carrier
    raise HTTPException(
        status_code=400,
        detail="id không tồn tại trên hệ thống"
    )
#cập nhật thông qua id
@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int,update_carrier: Carrier):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            for orther_carrier in carriers:
                if carrier["code"] == update_carrier.code:
                    raise HTTPException(
                        status_code=400,
                        detail="code không được trùng lập"
                    )
            carrier["code"] = update_carrier.code
            carrier["name"] = update_carrier.name
            carrier["max_weight_capacity"] = update_carrier.max_weight_capacity
            carrier["status"] = update_carrier.status
            return {
                "message":"cập nhật thành công",
                "data": carrier
            }
    raise HTTPException(
        status_code=400,
        detail="không có id trên hệ thống "
    )
@app.delete("/carriers/{carrier_id}")
def del_carrier(carrier_id: int):
    for i in range(len(carriers)):
        if carriers[i]["id"] == carrier_id:
            del_carrier_data = carriers.pop(i)
            return{
                "message":"đã xóa thành công",
                "data": del_carrier_data
            }
    raise HTTPException(
        status_code=400,
        detail="không tìm thấy id cần xóa"
    )