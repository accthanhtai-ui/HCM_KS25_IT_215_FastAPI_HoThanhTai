from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class WarehouseCreate(BaseModel):
    warehouse_name: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)


class PackageResponse(BaseModel):
    package_code: str
    weight: float

    model_config = ConfigDict(from_attributes=True)


class WarehouseDetailResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    package: list[PackageResponse]

    model_config = ConfigDict(from_attributes=True)


class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None


class WaybillResponse(BaseModel):
    id: int
    tracking_number: str
    shipping_status: str

    model_config = ConfigDict(from_attributes=True)