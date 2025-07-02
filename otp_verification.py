import streamlit as st
import smtplib
from email.message import EmailMessage
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_email(email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Verification Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f'Your One-Time Password (OTP) is: {otp}\n\nDo not share this code with anyone.')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f" Failed to send OTP. Error: {e}")
        return False

# --- Streamlit UI ---
st.title(" OTP Verification System")

# Initialize session state
if 'otp' not in st.session_state:
    st.session_state.otp = None
if 'tries' not in st.session_state:
    st.session_state.tries = 3
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

email_input = st.text_input("Enter your email address:")

if st.button("Send OTP"):
    if email_input:
        otp = generate_otp()
        st.session_state.otp = otp
        st.session_state.tries = 3
        if send_otp_via_email(email_input, otp):
            st.success(f" OTP sent to {email_input}")
            st.session_state.email_sent = True
    else:
        st.warning(" Please enter a valid email address.")

if st.session_state.email_sent and st.session_state.tries > 0:
    user_input = st.text_input("Enter the OTP received:")

    if st.button("Verify OTP"):
        if user_input == st.session_state.otp:
            st.success(" Access Granted. OTP Verified Successfully.")
            st.session_state.otp = None  # Reset for safety
        else:
            st.session_state.tries -= 1
            if st.session_state.tries > 0:
                st.error(f" Incorrect OTP. {st.session_state.tries} attempt(s) remaining.")
            else:
                st.error(" Too many incorrect attempts. Access Denied.")
                st.session_state.otp = None


