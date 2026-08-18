from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(product_id: int, db: Session):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def create_product(product: ProductCreate, db: Session):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def update_product(
        product_id: int,
        product: ProductCreate,
        db: Session
):
    db_product = get_product_by_id(
        product_id,
        db
    )

    if not db_product:
        return None

    db_product.name = product.name
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(
        product_id: int,
        db: Session
):
    db_product = get_product_by_id(
        product_id,
        db
    )

    if not db_product:
        return None

    db.delete(db_product)
    db.commit()

    return db_product