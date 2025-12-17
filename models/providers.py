from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    experience = Column(String)
    location = Column(String)
    bio = Column(String)
    role = Column(String, default="user")
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="providers")
    bookings = relationship("Booking", back_populates="provider")
    reviews = relationship("Review", back_populates="provider")
    provider_services = relationship("ProviderService", back_populates="provider")
