from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.users import User
from schemas.user_schema import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        return {"error": "Email already exists"}
    if db.query(User).filter(User.phone == user.phone).first():
        return {"error": "Phone number already exists"}
    new_user = User(name=user.name, email=user.email, phone=user.phone, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/all")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if users:
        return users
    return {"message": "No users found"}


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    return user


@router.put("/update/{user_id}")
def update_user(user_id: int, update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    existing_email = (
        db.query(User).filter(User.email == update.email, User.id != user_id).first()
    )
    if existing_email:
        return {"error": "Email already used by another user"}
    existing_phone = (
        db.query(User).filter(User.phone == update.phone, User.id != user_id).first()
    )
    if existing_phone:
        return {"error": "Phone already used by another user"}
    user.name = update.name
    user.email = update.email
    user.phone = update.phone
    user.role = update.role
    db.commit()
    db.refresh(user)
    return {"updated_user": user}


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
