from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import ProductCreate, ProductResponse

import services as product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
        db: Session = Depends(get_db)
):
    return product_service.get_all_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
        product_id: int,
        db: Session = Depends(get_db)
):
    product = product_service.get_product_by_id(
        product_id,
        db
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post(
    "",
    response_model=ProductResponse
)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db)
):
    return product_service.create_product(
        product,
        db
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
        product_id: int,
        product: ProductCreate,
        db: Session = Depends(get_db)
):
    updated_product = product_service.update_product(
        product_id,
        product,
        db
    )

    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product


@router.delete("/{product_id}")
def delete_product(
        product_id: int,
        db: Session = Depends(get_db)
):
    deleted_product = product_service.delete_product(
        product_id,
        db
    )

    if not deleted_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Delete successfully"
    }