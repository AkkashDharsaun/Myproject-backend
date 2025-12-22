from sqlalchemy import Column, String, Boolean, DateTime
from database import Base

class College(Base):
    __tablename__ = "colleges"

    collegeId = Column(String, primary_key=True, index=True)

    collegeName = Column(String, nullable=False)
    collegeType = Column(String, nullable=False)

    country = Column(String)
    stateOrProvince = Column(String)
    city = Column(String)
    postalCode = Column(String)

    collegeEmail = Column(String, unique=True, index=True, nullable=False)
    contactNumber = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    # 🔐 PAYMENT FIELDS
    isActive = Column(Boolean, default=False)
    planType = Column(String, default="YEARLY")
    planExpiry = Column(DateTime, nullable=True)
    paymentId = Column(String, nullable=True)



