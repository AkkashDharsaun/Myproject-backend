from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import College
from schemas import LoginData, CollegeRegister
from auth import hash_password, verify_password

router = APIRouter(prefix="", tags=["Auth"])  # later /auth use panna mudiyum


# ================= REGISTER =================
@router.post("/registerCollege")
def register_college(data: CollegeRegister, db: Session = Depends(get_db)):

    # Duplicate email check
    if db.query(College).filter(College.collegeEmail == data.collegeEmail).first():
        raise HTTPException(status_code=400, detail="Email is Already Registered")

    # Duplicate phone number check
    if db.query(College).filter(College.contactNumber == data.contactNumber).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")

    # Same password check
    hashed_password = hash_password(data.password)
    if db.query(College).filter(College.password == hashed_password).first():
        raise HTTPException(status_code=400, detail="Give a different strong password")

    college = College(
        collegeId=data.collegeId,
        collegeName=data.collegeName,
        collegeType=data.collegeType,
        country=data.country,
        stateOrProvince=data.stateOrProvince,
        city=data.city,
        postalCode=data.postalCode,
        collegeEmail=data.collegeEmail,
        contactNumber=str(data.contactNumber),
        password=hashed_password,
    )

    db.add(college)
    db.commit()

    return {"message": "College registered successfully"}


# ================= LOGIN =================
@router.post("/DashboardLogin")
def dashboard_login(data: LoginData, db: Session = Depends(get_db)):

    college = (
        db.query(College).filter(College.collegeEmail == data.collegeEmail).first()
    )

    if not college or not verify_password(data.password, college.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}


# ================= FORGET PASSWORD =================
@router.post("/forget-password")
def forget_password(data: LoginData, db: Session = Depends(get_db)):
    college = (
        db.query(College).filter(College.collegeEmail == data.collegeEmail).first()
    )

    if not college:
        raise HTTPException(status_code=404, detail="College not registered")

    if not is_strong_password(data.password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain uppercase, lowercase, number & symbol",
        )

    college.password = hash_password(data.password)
    db.commit()

    return {"message": "Password reset successful"}
