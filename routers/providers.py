from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.providers import Provider
from models.users import User
from schemas.provider_schema import (
    ProviderCreate,
    ProviderUpdate,
    ProviderResponse
)

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/create", response_model=ProviderResponse)
def create_provider(
    provider: ProviderCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == provider.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    new_provider = Provider(**provider.model_dump())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider

@router.get("/all", response_model=list[ProviderResponse])
def get_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()

@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.put("/update/{provider_id}", response_model=ProviderResponse)
def update_provider(
    provider_id: int,
    update: ProviderUpdate,
    db: Session = Depends(get_db)
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    user = db.query(User).filter(User.id == update.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    for key, value in update.model_dump().items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider

@router.delete("/delete/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()
    return {"message": "Provider deleted successfully"}
