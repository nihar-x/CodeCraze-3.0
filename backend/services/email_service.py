import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SENDER_NAME = os.getenv("SMTP_SENDER_NAME", "ParkMate")
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"


class EmailService:

    @staticmethod
    def send_otp_email(recipient, otp):

        # Developer fallback
        if DEV_MODE or not SMTP_EMAIL or not SMTP_PASSWORD:
            print(f"⚠️ DEV MODE OTP for {recipient}: {otp}")
            return True

        try:
            subject = "Your ParkMate OTP Verification"

            html = f"""
            <html>
            <body style="font-family:Arial">
                <h2>ParkMate Verification</h2>
                <p>Your OTP code is:</p>
                <h1 style="color:#4CAF50">{otp}</h1>
                <p>This code will expire in 10 minutes.</p>
            </body>
            </html>
            """

            msg = MIMEMultipart()
            msg["From"] = f"{SMTP_SENDER_NAME} <{SMTP_EMAIL}>"
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.sendmail(SMTP_EMAIL, recipient, msg.as_string())

            return True

        except Exception as e:
            print("❌ Email sending failed:", e)
            return False