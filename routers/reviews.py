from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, SessionLocal
from models.reviews import Review
from schemas.reviews_schema import ReviewCreate

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/create")
def create_review(review: ReviewCreate):
    db = SessionLocal()
    new_review = Review(
        user_id = review.user_id,
        provider_id = review.provider_id,
        rating_service = review.rating_service,
        rating_provider = review.rating_provider,
        comment = review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    db.close()
    return new_review

@router.get("/all")
def get_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews if reviews else {"message": "No reviews found"}

@router.get("/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    return review if review else {"message": "Review not found"}

@router.put("/update/{review_id}")
def update_review(review_id: int, update: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return {"message": "Review not found"}

    review.user_id = update.user_id
    review.provider_id = update.provider_id
    review.rating_service = update.rating_service
    review.rating_provider = update.rating_provider
    review.comment = update.comment

    db.commit()
    db.refresh(review)
    return {"updated_review": review}

@router.delete("/delete/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return {"message": "Review not found"}

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}
