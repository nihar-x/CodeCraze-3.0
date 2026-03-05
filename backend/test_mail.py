import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

print(f"Testing with: {app.config['MAIL_USERNAME']} on {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")

with app.app_context():
    try:
        msg = Message(
            subject="ParkMate Test Email",
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]]  # Send to self
        )
        msg.body = "This is a test email from ParkMate backend configuration."
        mail.send(msg)
        print("✅ Success! Email sent.")
    except Exception as e:
        print(f"❌ Failed! Error: {e}")
