from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db
from models.bookings import Booking
from models.users import User
from models.services import Service
from models.providers import Provider
from schemas.bookings_schema import BookingCreate, BookingUpdate

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401)
    return user


# create booking
@router.post("", status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = db.query(Service).filter(Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    new_booking = Booking(
        user_id=current_user.id,
        service_id=booking.service_id,
        address=booking.address,
        city=booking.city,
        pincode=booking.pincode,
        date=booking.date,
        time=booking.time,
        instructions=booking.instructions,
        status="pending",
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {"message": "Booking created successfully", "booking_id": new_booking.id}


# get accepted bookings
@router.get("/accepted")
def get_accepted_bookings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id, Booking.status == "confirmed")
        .all()
    )


# get my bookings
@router.get("/my")
def get_my_bookings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()


# get booking by id
@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_id == current_user.id)
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


# delete booking
@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_id == current_user.id)
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled successfully"}


# get current provider
def get_current_provider(db: Session = Depends(get_db)):
    provider = db.query(Provider).first()
    if not provider:
        raise HTTPException(status_code=401, detail="Provider not found")
    return provider


#  USER → GET WHO ACCEPTED THE ORDER
@router.get("/my/accepted")
def get_who_accepted_my_booking(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    results = (
        db.query(Booking, Provider)
        .join(Provider, Booking.provider_id == Provider.id)
        .filter(Booking.user_id == current_user.id, Booking.status == "confirmed")
        .all()
    )

    response = []
    for booking, provider in results:
        response.append(
            {
                "booking_id": booking.id,
                "service_id": booking.service_id,
                "date": booking.date,
                "time": booking.time,
                "status": booking.status,
                "provider": {
                    "provider_id": provider.id,
                    "experience": provider.years_experience,
                    "location": provider.address,
                    "bio": provider.bio,
                },
            }
        )

    return response


# PROVIDER → PUT CONFIRMED → COMPLETED
@router.put("/provider/{booking_id}/complete")
def provider_complete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_provider: Provider = Depends(get_current_provider),
):
    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id,
            Booking.provider_id == current_provider.id,
            Booking.status == "confirmed",
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404, detail="Confirmed booking not found for this provider"
        )

    booking.status = "completed"
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking marked as completed by provider",
        "booking_id": booking.id,
        "status": booking.status,
    }


# PROVIDER → GET USERS WITH PENDING REQUESTS
@router.get("/provider/pending")
def get_provider_pending_bookings(
    db: Session = Depends(get_db),
    current_provider: Provider = Depends(get_current_provider),
):
    bookings = db.query(Booking).filter(Booking.status == "pending").all()

    return bookings


# PROVIDER → PUT PENDING → CONFIRMED
@router.put("/provider/{booking_id}/confirm")
def confirm_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_provider: Provider = Depends(get_current_provider),
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.status == "pending")
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Pending booking not found")

    booking.provider_id = current_provider.id
    booking.status = "confirmed"
    db.commit()

    return {
        "message": "Booking confirmed successfully",
        "booking_id": booking.id,
        "status": booking.status,
    }
