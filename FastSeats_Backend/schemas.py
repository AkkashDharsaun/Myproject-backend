from pydantic import BaseModel, EmailStr
from datetime import datetime

class LoginData(BaseModel):
    collegeEmail: EmailStr
    password: str


class CollegeRegister(BaseModel):
    collegeId: str
    collegeName: str
    collegeType: str
    country: str
    stateOrProvince: str
    city: str
    counsellingcode: int
    collegeEmail: EmailStr
    contactNumber: str
    password: str
    is_registered: bool = True
    paymentId: str
    isActive: bool
    planType: str
    planExpiry: datetime


class ForgetPassword(BaseModel):
    collegeEmail: EmailStr
    newPassword: str
