from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.Database import Base


class Warehouse(Base):
    __tablename__ = "warehouse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    package = relationship("Package", back_populates="warehouse")


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_code = Column(String(255), unique=True, nullable=False)
    weight = Column(Float, nullable=False)

    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)

    warehouse = relationship("Warehouse", back_populates="package")
    waybill = relationship("Waybill", back_populates="package", uselist=False)


class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String(255), unique=True, nullable=False)
    shipping_status = Column(String(255), nullable=False)

    package_id = Column(
        Integer,
        ForeignKey("packages.id"),
        unique=True,
        nullable=False
    )

    package = relationship("Package", back_populates="waybill")
        
    

    
        
        
  