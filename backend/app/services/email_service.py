import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

SENDER_EMAIL = "cybershield128@gmail.com"
SENDER_NAME = "Cyber Shield" 
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_email(to_email: str, subject: str, html_content: str):
    msg = EmailMessage()
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.set_content("This email requires an HTML-compatible email client.")
    msg.add_alternative(html_content, subtype="html")

    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()

    except Exception as e:
        print("Email sending failed:", str(e))
        raise
    
    
def send_verification_email(email, token):
    link = f"https://cybershield-449512407166.europe-west1.run.app/auth/verify-email?token={token}"

    html = f"""
    <h2>Verify your email</h2>
    <p>Click the button below to verify your account:</p>
    <a href="{link}" style="
        display:inline-block;
        padding:10px 20px;
        background-color:#4CAF50;
        color:white;
        text-decoration:none;
        border-radius:5px;
    ">Verify Email</a>
    <p>If you didn’t request this, ignore this email.</p>
    """

    send_email(email, "Verify your email", html)    
    
    
def send_reset_email(email, token):
    link = f"https://cybershield-449512407166.europe-west1.run.app/auth/reset-password?token={token}"

    html = f"""
    <h2>Reset your password</h2>
    <p>Click below to reset your password:</p>
    <a href="{link}" style="
        display:inline-block;
        padding:10px 20px;
        background-color:#f44336;
        color:white;
        text-decoration:none;
        border-radius:5px;
    ">Reset Password</a>
    <p>This link expires in 15 minutes.</p>
    """

    send_email(email, "Reset your password", html)