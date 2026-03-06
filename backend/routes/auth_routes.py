import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from models.user_model import create_user, get_user_by_email, update_user_password
from config.db import otps_collection
from services.email_service import EmailService

auth_bp = Blueprint("auth", __name__)


# Redundant send_otp_email function removed - using EmailService instead


@auth_bp.route("/auth/send-signup-otp", methods=["POST"])
def send_signup_otp():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Check if user already exists
        if get_user_by_email(email):
            return jsonify({"error": "An account with this email already exists"}), 409

        otp = str(random.randint(100000, 999999))

        # Save OTP with 10-minute expiration (enforced by TTL index if configured)
        otps_collection.update_one(
            {"email": email},
            {"$set": {"otp": otp, "createdAt": datetime.utcnow()}},
            upsert=True,
        )

        # Trigger EmailService
        EmailService.send_otp_email(email, otp, "Sign Up")
        return jsonify({"message": "OTP sent to your email"}), 200

    except Exception as e:
        print("Send OTP error:", e)
        return jsonify({"error": "Failed to send OTP"}), 500


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email", "").strip().lower()
        password = data.get("password")
        otp_received = data.get("otp")

        if not all([name, email, password, otp_received]):
            return jsonify({"error": "All fields are required"}), 400

        # Verify OTP
        otp_record = otps_collection.find_one({"email": email})
        if not otp_record or otp_record["otp"] != otp_received:
            return jsonify({"error": "Invalid or expired OTP"}), 401

        # Delete OTP after successful verification
        otps_collection.delete_one({"email": email})

        # Create user
        create_user(name, email, password)
        user = get_user_by_email(email)

        return jsonify({"message": "Registration successful", "user": user}), 201

    except Exception as e:
        print("Registration error:", e)
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "No account found with this email"}), 404

        if user["password"] != password:
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({"message": "Login successful", "user": user}), 200

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route("/auth/send-forgot-otp", methods=["POST"])
def send_forgot_otp():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Check if user exists
        if not get_user_by_email(email):
            return jsonify({"error": "No account found with this email"}), 404

        otp = str(random.randint(100000, 999999))

        otps_collection.update_one(
            {"email": email},
            {"$set": {"otp": otp, "createdAt": datetime.utcnow()}},
            upsert=True,
        )

        EmailService.send_otp_email(email, otp, "Password Reset")
        return jsonify({"message": "Password reset OTP sent to your email"}), 200

    except Exception as e:
        print("Forgot OTP error:", e)
        return jsonify({"error": "Failed to send reset code"}), 500


@auth_bp.route("/auth/verify-forgot-otp", methods=["POST"])
def verify_forgot_otp():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        otp_received = data.get("otp")

        if not email or not otp_received:
            return jsonify({"error": "Email and OTP are required"}), 400

        otp_record = otps_collection.find_one({"email": email})
        if not otp_record or otp_record["otp"] != otp_received:
            return jsonify({"error": "Invalid or expired OTP"}), 401

        return jsonify({"message": "OTP verified successfully"}), 200

    except Exception:
        return jsonify({"error": "Verification failed"}), 500


@auth_bp.route("/auth/reset-password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        otp_received = data.get("otp")
        new_password = data.get("newPassword") or data.get("password")

        if not all([email, otp_received, new_password]):
            return jsonify({"error": "Missing required fields"}), 400

        otp_record = otps_collection.find_one({"email": email})
        if not otp_record or otp_record["otp"] != otp_received:
            return jsonify({"error": "Invalid or expired session"}), 401

        # Reset password
        update_user_password(email, new_password)

        # Clean up OTP
        otps_collection.delete_one({"email": email})

        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        print("Reset password error:", e)
        return jsonify({"error": "Failed to reset password"}), 500
