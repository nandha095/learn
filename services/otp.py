# blog/services/otp.py
import random
from datetime import datetime, timedelta

otp_store = {}

def generate_otp(email: str) -> str:
    otp = f"{random.randint(100000, 999999)}"
    # print(f"[DEBUG] Generated OTP for {email}: {otp}") 
    otp_store[email] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    return otp


def verify_otp(email: str, otp: str) -> bool:
    data = otp_store.get(email)
    if not data:
        # print(f"[DEBUG] No OTP found for {email}")
        return False
    if datetime.utcnow() > data["expires"]:
        # print(f"[DEBUG] OTP for {email} expired at {data['expires']}")
        return False
    if data["otp"] != otp:
        # print(f"[DEBUG] OTP mismatch for {email}: expected {data['otp']}, got {otp}")
        return False
    return True


def send_otp_email(email: str, otp: str, purpose: str = "OTP Verification"):
    subject = f"{purpose} - OTP Code"
    message = f"""
Hello,

Your OTP code for {purpose.lower()} is: {otp}

If you did not request this, please ignore.

Thanks,  
FastAPI Blog Team
"""
    


