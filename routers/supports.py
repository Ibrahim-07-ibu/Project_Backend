from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, SessionLocal
from models.supports import Support
from schemas.supports_schema import SupportCreate   

router = APIRouter(prefix="/supports",tags={"Supports"})

@router.post("/create")
def create_support(support:SupportCreate):
    db = SessionLocal()
    new_support = Support(
        user_id = support.user_id,
        subject = support.subject,
        message = support.message
    )

    db.add(new_support)
    db.commit()
    db.refresh(new_support)
    db.close()
    return new_support

@router.get("/all")
def get_support(db: Session = Depends(get_db)):
    supports = db.query(Support).all()
    return supports if supports else {"message": "No Supports found"}

@router.get("/{support_id}")
def get_support(support_id: int, db: Session = Depends(get_db)):
    support = db.query(Support).filter(Support.id == support_id).first()
    return support if support else {"message": "Support not found"}
