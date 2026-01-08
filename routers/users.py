from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db
from models.users import User
from models.providers import Provider
from schemas.user_schema import UserRegister, UserLogin

router = APIRouter(prefix="/api/auth", tags=["Auth"])

#user registration
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password, 
        phone=user.phone,
        address=user.address,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }
#user login
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": db_user.id
    }


#get all users
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()
