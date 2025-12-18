from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class ProviderService(Base):
    __tablename__ = "provider_services"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), index=True)
    service_id = Column(Integer, ForeignKey("services.id"), index=True)
    price = Column(Integer)
    availability = Column(Boolean)

    provider = relationship("Provider", back_populates="provider_services")
    service = relationship("Service", back_populates="provider_services")
