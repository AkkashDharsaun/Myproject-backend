from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import College
from schemas import LoginData, CollegeRegister
from auth import hash_password, verify_password

router = APIRouter(prefix="", tags=["Auth"])


# ================= DASHBOARD LOGIN =================
@router.post("/DashboardLogin")
def dashboard_login(data: LoginData, db: Session = Depends(get_db)):

    college = (
        db.query(College).filter(College.collegeEmail == data.collegeEmail).first()
    )

    if not college.is_active:
        raise HTTPException(
            status_code=403, detail="Account inactive. Payment required"
        )
    if college and not verify_password(data.password, college.password):
        raise HTTPException(status_code=401, detail="Password is incorrect")

    if not college and not verify_password(data.password, college.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "collegeId": college.collegeId,
        "collegeName": college.collegeName,
        "collegeEmail": college.collegeEmail,
        "collegeType": college.collegeType,
        "isActive": college.is_active,
        "isRegistered": college.is_registered,  # 🔥 NEW
    }


# ================= REGISTER =================
@router.post("/registerCollege")
def register_college(data: CollegeRegister, db: Session = Depends(get_db)):

    # 🔁 Duplicate email
    if db.query(College).filter(College.collegeEmail == data.collegeEmail).first():
        raise HTTPException(
            status_code=400,
            detail="Email is Already Registered",
        )

    # 🔁 Duplicate phone
    if db.query(College).filter(College.contactNumber == data.contactNumber).first():
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists",
        )

    # 🔐 Password hash
    hashed_password = hash_password(data.password)

    college = College(
        collegeId=data.collegeId,
        collegeName=data.collegeName,
        collegeType=data.collegeType,
        country=data.country,
        stateOrProvince=data.stateOrProvince,
        city=data.city,
        counsellingcode=data.counsellingcode,
        collegeEmail=data.collegeEmail,
        contactNumber=str(data.contactNumber),
        password=hashed_password,
        payment_id=data.paymentId,
        is_active=data.isActive,
        plan_type=data.planType,
        plan_expiry=data.planExpiry,
        is_registered=True,  # 🔥 IMPORTANT
    )

    db.add(college)
    db.commit()

    return {"message": "College registered successfully"}


# ================= FORGET PASSWORD =================
@router.post("/forget-password")
def forget_password(data: LoginData, db: Session = Depends(get_db)):

    college = (
        db.query(College).filter(College.collegeEmail == data.collegeEmail).first()
    )

    if not college:
        raise HTTPException(
            status_code=404,
            detail="College not registered",
        )

    college.password = hash_password(data.password)
    db.commit()

    return {"message": "Password reset successful"}
