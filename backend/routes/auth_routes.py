import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from models.user_model import create_user, get_user_by_email
from utils.tokens import generate_token, verify_token

auth_bp = Blueprint("auth", __name__)


# ───────────────── MAGIC LINK AUTH ─────────────────

@auth_bp.route("/auth/send-magic-link", methods=["POST"])
def send_magic_link():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Generate signed token (timed)
        token = generate_token(email)

        # Build magic link
        # Use frontend URL from .env or fallback
        frontend_url = os.getenv("FRONTEND_URL", "https://code-craze-3-0.vercel.app")
        magic_link = f"{frontend_url}/magic-login?token={token}"

        msg = Message(
            subject="Your ParkMate Login Link",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        msg.body = f"""
Hello,

You requested a login link for ParkMate. Click the button or link below to sign in:

{magic_link}

This link is valid for 10 minutes.

If you did not request this, you can safely ignore this email.

Regards,
ParkMate Team
"""
        # Alternatively, send HTML if needed, but keeping it simple for now.

        mail = current_app.extensions["mail"]
        mail.send(msg)

        print(f"Magic link sent to {email}")
        return jsonify({"message": "Check your email for the magic login link!"}), 200

    except Exception as e:
        print("Magic link error:", str(e))
        return jsonify({"error": "Failed to send magic link. Please try again later."}), 500


@auth_bp.route("/auth/verify-magic-link", methods=["GET"])
def verify_magic_link():
    try:
        token = request.args.get("token")
        if not token:
            return jsonify({"error": "Login token is missing"}), 400

        # Verify token and extract email
        email = verify_token(token, expiration=600)  # 10 minutes expiration

        if not email:
            return jsonify({"error": "This link is invalid or has expired. Please request a new one."}), 401

        # Check if user exists
        user = get_user_by_email(email)

        if not user:
            # First-time user: Create account automatically
            # We use the prefix of the email as a placeholder name
            default_name = email.split("@")[0].capitalize()
            create_user(
                name=default_name,
                email=email,
                password="passwordless_auth", # Placeholder since we use magic links
                role="user"
            )
            user = get_user_by_email(email)

        # In a full JWT system, you'd generate a token here.
        # For this project's current state, we return user details for localStorage.
        return jsonify({
            "message": "Successfully authenticated",
            "user": user
        }), 200

    except Exception as e:
        print("Verify link error:", str(e))
        return jsonify({"error": "Authentication failed"}), 500


# ───────────────── LEGACY LOGIN (Optional) ─────────────────
# Keeping the standard password login for admin access or traditional users if any.
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "No account found with this email"}), 404

        if user["password"] != password:
            return jsonify({"error": "Invalid password"}), 401

        return jsonify({
            "message": "Login successful",
            "user": user
        }), 200

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Login failed"}), 500
