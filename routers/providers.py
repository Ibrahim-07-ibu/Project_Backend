from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, SessionLocal
from models.providers import Provider
from schemas.provider_schema import ProviderCreate

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/create")
def create_provider(provider: ProviderCreate):
    db = SessionLocal()
    new_provider = Provider(
        user_id = provider.user_id,
        experience = provider.experience,
        location = provider.location,
        bio = provider.bio,
        is_verified = provider.is_verified
    )
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    db.close()
    return new_provider

@router.get("/all")
def get_providers(db: Session = Depends(get_db)):
    providers = db.query(Provider).all()
    return providers if providers else {"message": "No providers found"}

@router.get("/{provider_id}")
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    return provider if provider else {"message": "Provider not found"}

@router.put("/update/{provider_id}")
def update_provider(provider_id: int, update: ProviderCreate, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return {"message": "Provider not found"}
    
    provider.user_id = update.user_id
    provider.experience = update.experience
    provider.location = update.location
    provider.bio = update.bio
    provider.is_verified = update.is_verified

    db.commit()
    db.refresh(provider)
    return {"updated_provider": provider}

@router.delete("/delete/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return {"message": "Provider not found"}

    db.delete(provider)
    db.commit()
    return {"message": "Provider deleted successfully"}
