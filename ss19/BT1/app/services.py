from sqlalchemy.orm import Session
from fastapi import HTTPException
import app.model as model
import app.schemas as schemas


def create_warehouse(db: Session, warehouse: schemas.WarehouseCreate):
    try:
        new_warehouse = model.Warehouse(**warehouse.model_dump())

        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)

        return new_warehouse

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Create warehouse failed")


def get_warehouse(db: Session, warehouse_id: int):
    warehouse = db.query(model.Warehouse).filter(
        model.Warehouse.id == warehouse_id
    ).first()

    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    return warehouse


def update_package(
    db: Session,
    package_id: int,
    package: schemas.PackageUpdate
):
    package_db = db.query(model.Package).filter(
        model.Package.id == package_id
    ).first()

    if not package_db:
        raise HTTPException(status_code=404, detail="Package not found")

    try:
        update_data = package.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(package_db, key, value)

        db.commit()
        db.refresh(package_db)

        return package_db

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Update failed")


def delete_waybill(db: Session, waybill_id: int):
    waybill = db.query(model.Waybill).filter(
        model.Waybill.id == waybill_id
    ).first()

    if not waybill:
        raise HTTPException(status_code=404, detail="Waybill not found")

    try:
        db.delete(waybill)
        db.commit()

        return {
            "message": "Delete successfully"
        }

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Delete failed")