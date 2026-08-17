from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from app.schemas.schemas import (
    MedicalRegister,
    MedicalLogin,
    TokenResponse,
    PrescriptionCreate
)

from app.services.medical_services import (
    register_medical_user,
    login_medical_user
)

from app.cores.jwt import create_access_token, verify_access_token


medical_router = APIRouter(
    prefix="/api/v1",
    tags=["MedCare"]
)


security = HTTPBearer()


@medical_router.post(
    "/medical/register"
)
def register(
    user: MedicalRegister
):
    return register_medical_user(
        user.username,
        user.password,
        user.role
    )


@medical_router.post(
    "/medical/login",
    response_model=TokenResponse
)
def login(
    user: MedicalLogin
):
    db_user = login_medical_user(
        user.username,
        user.password
    )

    access_token = create_access_token(
        db_user["username"],
        db_user["role"]
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@medical_router.post(
    "/prescriptions"
)
def create_prescription(
    prescription: PrescriptionCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_access_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    if user["role"] != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không đủ quyền hạn"
        )

    return {
        "message": "Tạo đơn thuốc thành công",
        "doctor": user["username"],
        "patient_name": prescription.patient_name,
        "medicine": prescription.medicine,
        "quantity": prescription.quantity
    }


@medical_router.get(
    "/prescriptions/view"
)
def view_prescriptions(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_access_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return {
        "message": "Xem đơn thuốc thành công",
        "username": user["username"],
        "role": user["role"]
    }