from dotenv import load_dotenv

load_dotenv()
from flask import Flask, jsonify
from flask_cors import CORS
from config.db import init_db
from routes.auth_routes import auth_bp
from routes.slot_routes import slot_bp
from routes.booking_routes import booking_bp
from routes.payment_routes import payment_bp
from routes.contact_routes import contact_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)

# Enable CORS
CORS(app)

# Blueprints are registered below

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(slot_bp, url_prefix="/api")
app.register_blueprint(booking_bp, url_prefix="/api")
app.register_blueprint(payment_bp, url_prefix="/api")
app.register_blueprint(contact_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")


@app.route("/")
def home():
    return jsonify({"message": "🚗 ParkMate backend is running!", "status": "ok"})


@app.route("/api")
def api_root():
    return jsonify({"message": "ParkMate API (MongoDB)", "database": "parkmate_db"})


# Initialize DB
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
