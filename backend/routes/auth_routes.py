from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from models.user_model import create_user, get_user_by_email, update_user_password
from config.db import otps_collection
import random

auth_bp = Blueprint("auth", __name__)


# ───────────────── SEND SIGNUP OTP ─────────────────
@auth_bp.route("/auth/send-signup-otp", methods=["POST"])
def send_signup_otp():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        existing = get_user_by_email(email)
        if existing:
            return jsonify({"error": "An account with this email already exists"}), 409

        otp = str(random.randint(100000, 999999))
        
        # Store in MongoDB
        otps_collection.update_one(
            {"email": email},
            {"$set": {"otp": otp, "createdAt": datetime.utcnow()}},
            upsert=True
        )

        msg = Message(
            subject="ParkMate Registration OTP",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        msg.body = f"""
Hello,

Your OTP for ParkMate registration is:

{otp}

This OTP is valid for 5 minutes.

Regards,
ParkMate Team
"""

        mail = current_app.extensions["mail"]
        mail.send(msg)

        print(f"Signup OTP sent to {email}: {otp}")

        return jsonify({"message": "OTP sent to email"}), 200

    except Exception as e:
        print("Detailed Email Error:", str(e))
        return jsonify({"error": f"Failed to send OTP email: {str(e)}"}), 500


# ───────────────── REGISTER USER ─────────────────
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        otp = data.get("otp", "")

        if not name or not email or not password or not otp:
            return jsonify({"error": "All fields including OTP are required"}), 400

        stored_record = otps_collection.find_one({"email": email})
        if not stored_record or stored_record.get("otp") != otp:
            return jsonify({"error": "Invalid or expired OTP"}), 401

        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        existing = get_user_by_email(email)
        if existing:
            return jsonify({"error": "An account with this email already exists"}), 409

        user_id = create_user(name, email, password)
        otps_collection.delete_one({"email": email})  # Clean up OTP after successful registration

        return jsonify({
            "message": "Account created successfully",
            "user": {
                "_id": str(user_id),
                "name": name,
                "email": email,
                "role": "user"
            }
        }), 201

    except Exception as e:
        print("Register error:", e)
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/signup", methods=["POST"])
def signup():
    return register()


# ───────────────── LOGIN ─────────────────
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
            "user": {
                "_id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user.get("role", "user"),
            }
        }), 200

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login_legacy():
    return login()


# ───────────────── FORGOT PASSWORD OTP ─────────────────
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        user = get_user_by_email(email)

        if not user:
            return jsonify({"error": "No account found with this email"}), 404

        otp = str(random.randint(100000, 999999))

        otps_collection.update_one(
            {"email": email},
            {"$set": {"otp": otp, "createdAt": datetime.utcnow()}},
            upsert=True
        )

        msg = Message(
            subject="ParkMate Password Reset OTP",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        msg.body = f"""
Hello,

Your OTP for resetting your ParkMate password is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this password reset, please ignore this email.

Regards,
ParkMate Team
"""

        mail = current_app.extensions["mail"]
        mail.send(msg)

        print(f"Password reset OTP sent to {email}: {otp}")

        return jsonify({
            "message": "OTP sent to email",
            "email": email
        }), 200

    except Exception as e:
        print("Detailed Email Error:", str(e))
        return jsonify({"error": f"Failed to send OTP email: {str(e)}"}), 500


# ───────────────── VERIFY OTP ─────────────────
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = request.get_json()

        email = data.get("email", "").strip().lower()
        otp = data.get("otp", "")

        if not email or not otp:
            return jsonify({"error": "Email and OTP are required"}), 400

        stored_record = otps_collection.find_one({"email": email})
        stored_otp = stored_record.get("otp") if stored_record else None

        if stored_otp != otp:
            return jsonify({"error": "Invalid or expired OTP"}), 401

        return jsonify({"message": "OTP verified"}), 200

    except Exception as e:
        print("OTP verify error:", e)
        return jsonify({"error": "OTP verification failed"}), 500


# ───────────────── RESET PASSWORD ─────────────────
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()

        email = data.get("email", "").strip().lower()
        new_password = data.get("newPassword", "")

        if not email or not new_password:
            return jsonify({"error": "Email and new password are required"}), 400

        if len(new_password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        update_user_password(email, new_password)

        # remove OTP after reset
        otps_collection.delete_one({"email": email})

        return jsonify({
            "message": "Password updated successfully"
        }), 200

    except Exception as e:
        print("Password reset error:", e)
        return jsonify({"error": "Password reset failed"}), 500
