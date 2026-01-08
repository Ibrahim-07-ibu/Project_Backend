from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db
from dependencies import get_current_user
from models.providers import Provider
from models.users import User

from schemas.provider_schema import (
    ProviderCreate,
    ProviderLogin,
    ProviderUpdate,
    ProviderResponse,
)

router = APIRouter(prefix="/providers", tags=["Providers"])


def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated"
        )
    return user


# create provider
@router.post("/create", response_model=ProviderResponse)
def create_provider(
    provider: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_provider = Provider(user_id=current_user.id, **provider.model_dump())

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider


# login provider
@router.post("/provider/login")
def login_provider(user: ProviderLogin, db: Session = Depends(get_db)):

    db_provider = db.query(Provider).filter(Provider.email == user.email).first()

    if not db_provider or db_provider.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "provider_id": db_provider.id}


# get all providers
@router.get("/all", response_model=list[ProviderResponse])
def get_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()


# get provider by id
@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


# update provider
@router.put("/update/{provider_id}", response_model=ProviderResponse)
def update_provider(
    provider_id: int, update: ProviderUpdate, db: Session = Depends(get_db)
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    for key, value in update.model_dump().items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider


# delete provider
@router.delete("/delete/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()
    return {"message": "Provider deleted successfully"}
