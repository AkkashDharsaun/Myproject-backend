from sqlalchemy import Column, String
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
    collegeEmail = Column(String, unique=True, index=True)
    contactNumber = Column(String)
    password = Column(String)

