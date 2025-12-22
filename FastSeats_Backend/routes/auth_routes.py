from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import razorpay
from dotenv import load_dotenv

from database import get_db
from models import College
from schemas import LoginData, CollegeRegister, ForgetPassword

from auth import hash_password, verify_password

load_dotenv()

router = APIRouter(prefix="", tags=["Auth"])

# 🔐 Razorpay client (SECRET KEY HERE)
client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))


# ================= CREATE ORDER =================
@router.post("/create-order")
def create_order():
    order = client.order.create({
        "amount": 10,  # ₹1 = 100 paise
        "currency": "INR",
        "payment_capture": 1
    })
    return {
        "orderId": order["id"],
        "amount": order["amount"]
    }


# ================= VERIFY PAYMENT =================
@router.post("/verify-payment")
def verify_payment(data: dict):
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
        return {"status": "verified"}
    except:
        raise HTTPException(status_code=400, detail="Payment verification failed")


# ================= REGISTER COLLEGE =================
@router.post("/registerCollege")
def register_college(data: CollegeRegister, db: Session = Depends(get_db)):

    if db.query(College).filter(College.collegeEmail == data.collegeEmail).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(College).filter(College.contactNumber == data.contactNumber).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")

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
        password=hash_password(data.password),

        isActive=True,
        planType="YEARLY",
        planExpiry=datetime.now() + timedelta(days=365),
        paymentId=data.paymentId
    )

    db.add(college)
    db.commit()
    db.refresh(college)

    return {
        "message": "Payment verified & College registered",
        "planExpiry": college.planExpiry
    }
