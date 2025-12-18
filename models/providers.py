from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    experience = Column(String)    
    location = Column(String, nullable=False)
    bio = Column(String, nullable=True)

    role = Column(String, default="provider")
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="providers")
    bookings = relationship("Booking", back_populates="provider")
    reviews = relationship("Review", back_populates="provider")
    provider_services = relationship("ProviderService", back_populates="provider")
