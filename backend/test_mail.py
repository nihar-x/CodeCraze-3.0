import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

smtp_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
smtp_port = int(os.getenv("MAIL_PORT", 587))
sender_email = os.getenv("MAIL_USERNAME")
sender_password = os.getenv("MAIL_PASSWORD")

print(f"Testing with: {sender_email} on {smtp_server}:{smtp_port}")

try:
    if not sender_email or not sender_password:
        raise ValueError(
            "MAIL_USERNAME or MAIL_PASSWORD is not set in environment variables."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "ParkMate Test Email"
    msg["From"] = sender_email
    msg["To"] = sender_email

    text = "This is a test email from ParkMate backend using standard smtplib."
    msg.attach(MIMEText(text, "plain"))

    server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, sender_email, msg.as_string())
    server.quit()

    print("✅ Success! Email sent using standard libraries.")
except Exception as e:
    print(f"❌ Failed! Error: {e}")
