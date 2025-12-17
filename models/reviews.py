from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    rating_service = Column(Integer)
    rating_provider = Column(Integer)
    comment = Column(String)

    user = relationship("User", back_populates="reviews")
    provider = relationship("Provider", back_populates="reviews")
    service = relationship("Service", back_populates="reviews")
