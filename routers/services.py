from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, SessionLocal
from models.services import Service
from schemas.services_schema import ServiceCreate

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/create")
def create_service(service: ServiceCreate):
    db = SessionLocal()
    new_service = Service(
        name=service.name,
        price = service.price,
        description=service.description
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    db.close()
    return new_service

@router.get("/all")
def get_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services if services else {"message": "No services found"}

@router.get("/{service_id}")
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    return service if service else {"message": "Service not found"}

@router.put("/update/{service_id}")
def update_service(service_id: int, update: ServiceCreate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return {"message": "Service not found"}

    service.name = update.name
    service.price = update.price
    service.description = update.description

    db.commit()
    db.refresh(service)
    return {"updated_service": service}

@router.delete("/delete/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return {"message": "Service not found"}

    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}
