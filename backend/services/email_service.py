import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    smtp_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("MAIL_PORT", 587))
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    sender_name = os.getenv("MAIL_SENDER_NAME", "ParkMate Support")

    @classmethod
    def send_otp_email(cls, recipient, otp, purpose="verification"):
        """Sends a 6-digit OTP to the recipient with an HTML template."""

        # Developer Mode: Fallback if credentials are not configured
        if not cls.sender_email or not cls.sender_password:
            print(
                f"\n[DEV MODE] Skipping real email sending. OTP for {recipient}: {otp}\n"
            )
            return True

        # HTML Email Template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <style>
                body {{ font-family: 'Inter', Arial, sans-serif; background-color: #f7f9fc; margin: 0; padding: 20px; }}
                .container {{ max-width: 480px; margin: 20px auto; background: #ffffff; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
                .logo {{ font-size: 24px; font-weight: 800; color: #7c3aed; margin-bottom: 30px; text-align: center; letter-spacing: -0.5px; }}
                h1 {{ font-size: 20px; color: #1f2937; margin-bottom: 10px; text-align: center; }}
                p {{ font-size: 15px; color: #6b7280; line-height: 1.6; text-align: center; }}
                .otp-card {{ background: #f3f0ff; border: 2px dashed #7c3aed; border-radius: 12px; padding: 20px; margin: 25px 0; }}
                .otp-code {{ font-size: 32px; font-weight: 800; letter-spacing: 12px; color: #7c3aed; text-align: center; margin: 0; }}
                .footer {{ font-size: 11px; color: #9ca3af; text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #f1f5f9; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: #7c3aed; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">PARKMATE</div>
                <h1>{purpose} Code</h1>
                <p>Hello! Use the following code to complete your {purpose.lower()}. This code will expire in 10 minutes.</p>
                
                <div class="otp-card">
                    <p class="otp-code">{otp}</p>
                </div>
                
                <p>If you didn't request this, you can safely ignore this email.</p>
                
                <div class="footer">
                    &copy; 2026 ParkMate Inc. · 123 Parking Way, Silicon Valley<br/>
                    Professional Secure OTP Services
                </div>
            </div>
        </body>
        </html>
        """

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Your ParkMate Code: {otp}"
            msg["From"] = f"{cls.sender_name} <{cls.sender_email}>"
            msg["To"] = recipient

            # Attach plain text and HTML parts
            plain_text = f"Your ParkMate OTP is: {otp}. It is valid for 10 minutes."
            msg.attach(MIMEText(plain_text, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            # Connect and send with retries
            retries = 3
            last_error = None

            for attempt in range(retries):
                try:
                    server = smtplib.SMTP(cls.smtp_server, cls.smtp_port, timeout=10)
                    server.starttls()
                    server.login(cls.sender_email, cls.sender_password)
                    server.sendmail(cls.sender_email, recipient, msg.as_string())
                    server.quit()
                    return True
                except Exception as attempt_error:
                    last_error = attempt_error
                    print(
                        f"SMTP retry {attempt + 1}/{retries} failed for {recipient}: {attempt_error}"
                    )
                    continue

            # If all retries fail, print to console as fallback (Developer mode fallback)
            print(
                f"\n[ERROR] SMTP failed after {retries} retries. Falling back to console."
            )
            print(
                f"[DEVELOPER FALLBACK] OTP for {recipient}: {otp} (Reason: {last_error})\n"
            )
            return False

        except Exception as e:
            print(f"Fatal error sending email to {recipient}: {e}")
            return False
