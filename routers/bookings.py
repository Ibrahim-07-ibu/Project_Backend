from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, SessionLocal
from models.bookings import Booking
from schemas.bookings_schema import BookingCreate
from models.users import User
from models.providers import Provider

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/create")
def create_booking(booking: BookingCreate):
    db = SessionLocal()
    new_booking = Booking(
        user_id=booking.user_id,
        provider_id=booking.provider_id,
        service_id=booking.service_id,
        date=booking.date,
        time=booking.time,
        address = booking.address,
        city=booking.city,
        pincode=booking.pincode,
        instructions=booking.instructions,
        status=booking.status
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    db.close()
    return new_booking

@router.get("/all")
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings if bookings else {"message": "No bookings found"}

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user if user else {"message": "Booking not found"}

@router.get("/{provider_id}")
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    return provider if provider else {"message": "Booking not found"}

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    return booking if booking else {"message": "Booking not found"}

@router.put("/update/{booking_id}")
def update_booking(booking_id: int, update: BookingCreate, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        return {"message": "Booking not found"}

    booking.user_id = update.user_id
    booking.provider_id = update.provider_id
    booking.service_id = update.service_id
    booking.date = update.date
    booking.time = update.time
    booking.address=update.address
    booking.city=update.city
    booking.pincode=update.city
    booking.instructions = update.instructions
    booking.status = update.status

    db.commit()
    db.refresh(booking)
    return {"updated_booking": booking}

@router.delete("/delete/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        return {"message": "Booking not found"}

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}
