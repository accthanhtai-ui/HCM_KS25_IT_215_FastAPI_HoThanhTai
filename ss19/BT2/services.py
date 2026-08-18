from sqlalchemy.orm import Session
from fastapi import HTTPException

import model
import schemas


def create_clinic(db: Session, clinic: schemas.ClinicCreate):
    try:
        new_clinic = model.Clinic(**clinic.model_dump())

        db.add(new_clinic)
        db.commit()
        db.refresh(new_clinic)

        return new_clinic

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Create clinic failed")


def get_clinic(db: Session, clinic_id: int):
    clinic = db.query(model.Clinic).filter(
        model.Clinic.id == clinic_id
    ).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    return clinic


def update_doctor(
    db: Session,
    doctor_id: int,
    doctor: schemas.DoctorUpdate
):
    doctor_db = db.query(model.Doctor).filter(
        model.Doctor.id == doctor_id
    ).first()

    if not doctor_db:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        update_data = doctor.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(doctor_db, key, value)

        db.commit()
        db.refresh(doctor_db)

        return doctor_db

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Update failed")


def delete_license(db: Session, license_id: int):
    license = db.query(model.License).filter(
        model.License.id == license_id
    ).first()

    if not license:
        raise HTTPException(status_code=404, detail="License not found")

    try:
        db.delete(license)
        db.commit()

        return {
            "message": "Delete successfully"
        }

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Delete failed")