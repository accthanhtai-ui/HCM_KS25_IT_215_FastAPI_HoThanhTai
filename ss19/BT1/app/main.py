from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from app.Database import Base, engine, get_db

import app.model as model
import app.schemas as schemas
import app.services as services
app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post(
    "/warehouses",
    status_code=status.HTTP_201_CREATED
)
def create_warehouse(
    warehouse: schemas.WarehouseCreate,
    db: Session = Depends(get_db)
):
    return services.create_warehouse(db=db, warehouse=warehouse)


@app.get(
    "/warehouses/{warehouse_id}",
    response_model=schemas.WarehouseDetailResponse
)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    return services.get_warehouse(db=db, warehouse_id=warehouse_id)


@app.patch("/packages/{package_id}")
def update_package(
    package_id: int,
    package: schemas.PackageUpdate,
    db: Session = Depends(get_db)
):
    return services.update_package(
        db=db,
        package_id=package_id,
        package=package
    )


@app.delete("/waybills/{waybill_id}")
def delete_waybill(
    waybill_id: int,
    db: Session = Depends(get_db)
):
    return services.delete_waybill(
        db=db,
        waybill_id=waybill_id
    )