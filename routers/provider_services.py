from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, SessionLocal
from models.provider_services import ProviderService
from schemas.provider_services_schema import ProviderServiceCreate

router = APIRouter(prefix="/provider-services", tags=["Provider Services"])

@router.post("/create")
def create_provider_service(ps: ProviderServiceCreate):
    db = SessionLocal()
    new_ps = ProviderService(
        provider_id=ps.provider_id,
        service_id=ps.service_id,
        price=ps.price,
        availability=ps.availability
    )
    db.add(new_ps)
    db.commit()
    db.refresh(new_ps)
    db.close()
    return new_ps

@router.get("/all")
def get_provider_services(db: Session = Depends(get_db)):
    ps = db.query(ProviderService).all()
    return ps if ps else {"message": "No provider services found"}

@router.get("/{ps_id}")
def get_provider_service(ps_id: int, db: Session = Depends(get_db)):
    ps = db.query(ProviderService).filter(ProviderService.id == ps_id).first()
    return ps if ps else {"message": "Provider service not found"}

@router.put("/update/{ps_id}")
def update_provider_service(ps_id: int, update: ProviderServiceCreate, db: Session = Depends(get_db)):
    ps = db.query(ProviderService).filter(ProviderService.id == ps_id).first()
    if not ps:
        return {"message": "Provider service not found"}

    ps.provider_id = update.provider_id
    ps.service_id = update.service_id
    ps.price = update.price
    ps.availability = update.availability

    db.commit()
    db.refresh(ps)
    return {"updated_provider_service": ps}

@router.delete("/delete/{ps_id}")
def delete_provider_service(ps_id: int, db: Session = Depends(get_db)):
    ps = db.query(ProviderService).filter(ProviderService.id == ps_id).first()
    if not ps:
        return {"message": "Provider service not found"}

    db.delete(ps)
    db.commit()
    return {"message": "Provider service deleted successfully"}
