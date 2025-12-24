from sqlalchemy import Column, String, Boolean, DateTime,Integer
from database import Base

class College(Base):
    __tablename__ = "colleges"

    collegeId = Column(String, primary_key=True, index=True)

    collegeName = Column(String, nullable=False)
    collegeType = Column(String, nullable=False)

    country = Column(String)
    stateOrProvince = Column(String)
    city = Column(String)
    counsellingcode = Column(Integer)

    collegeEmail = Column(String, unique=True, index=True, nullable=False)
    contactNumber = Column(String, unique=True, nullable=False)
    is_registered = Column(Boolean, default=False)
    password = Column(String, nullable=False)

    # 💳 Payment fields
    payment_id = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    plan_type = Column(String)
    plan_expiry = Column(DateTime)  



