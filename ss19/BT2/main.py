from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from Database import Base, engine, get_db

import model
import schemas
import services

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post(
    "/clinics",
    status_code=status.HTTP_201_CREATED
)
def create_clinic(
    clinic: schemas.ClinicCreate,
    db: Session = Depends(get_db)
):
    return services.create_clinic(db=db, clinic=clinic)


@app.get(
    "/clinics/{clinic_id}",
    response_model=schemas.ClinicDetailResponse
)
def get_clinic(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    return services.get_clinic(db=db, clinic_id=clinic_id)


@app.patch("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    doctor: schemas.DoctorUpdate,
    db: Session = Depends(get_db)
):
    return services.update_doctor(
        db=db,
        doctor_id=doctor_id,
        doctor=doctor
    )


@app.delete("/licenses/{license_id}")
def delete_license(
    license_id: int,
    db: Session = Depends(get_db)
):
    return services.delete_license(
        db=db,
        license_id=license_id
    )