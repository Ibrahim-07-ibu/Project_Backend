from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from models.reviews import Review
from schemas.reviews_schema import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

#create review
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    new_review = Review(
        user_id=1,  
        service_id=review.service_id,
        provider_id=review.provider_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review

#get my reviews
@router.get("/my/reviews", response_model=List[ReviewResponse])
def get_my_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews
