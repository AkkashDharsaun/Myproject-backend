from pydantic import BaseModel, EmailStr


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
    postalCode: str
    collegeEmail: EmailStr
    contactNumber: str
    password: str


class ForgetPassword(BaseModel):
    collegeEmail: EmailStr
    newPassword: str
