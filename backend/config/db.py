import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

# ─────────────────────────────────────────
# Load environment variables
# ─────────────────────────────────────────
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "parkmate_db")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in .env file")

# ─────────────────────────────────────────
# Connect to MongoDB
# ─────────────────────────────────────────
try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")  # test connection
    print("✅ MongoDB connected successfully")
except ConnectionFailure as e:
    raise RuntimeError(f"❌ MongoDB connection failed: {e}")

db = client[DB_NAME]

# ─────────────────────────────────────────
# Collections
# ─────────────────────────────────────────
users_collection = db["users"]
slots_collection = db["slots"]
bookings_collection = db["bookings"]
payments_collection = db["payments"]
otps_collection = db["otps"]


# ─────────────────────────────────────────
# Initialize Database
# ─────────────────────────────────────────
def init_db():
    """
    Seeds parking slots if empty and ensures indexes exist.
    """

    # ── Frontend constants (sync with Availability.jsx)
    LOCATIONS = [
        "CityMall",
        "Downtown Parking Hub",
        "Airport Terminal A",
        "Airport Terminal B",
        "Mall Central Parking",
        "Tech Park Zone 1",
        "Railway Station Lot",
    ]

    FLOORS = ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Basement"]

    existing_count = slots_collection.count_documents({})
    existing_locations = (
        set(slots_collection.distinct("location")) if existing_count > 0 else set()
    )
    expected_locations = set(LOCATIONS)

    # ──────────────────────────────────────
    # Reseed slots if empty or outdated
    # ──────────────────────────────────────
    if existing_count == 0 or not expected_locations.issubset(existing_locations):

        if existing_count > 0:
            slots_collection.drop()
            print("🔄 Reseeding parking slots (location list changed)")

        rows = ["A", "B", "C", "D"]
        cols = [1, 2, 3, 4]
        prices = [30, 40, 50, 60]

        slot_data = []
        price_idx = 0

        for loc in LOCATIONS:
            for flr in FLOORS:
                for row in rows:
                    for col in cols:
                        slot_data.append(
                            {
                                "slot_number": f"{row}{col}",
                                "location": loc,
                                "floor": flr,
                                "status": "available",
                                "price": prices[price_idx % len(prices)],
                            }
                        )
                        price_idx += 1

        slots_collection.insert_many(slot_data)

        print(f"✅ Seeded {len(slot_data)} parking slots")

    else:
        print(f"ℹ️ Slots already exist: {existing_count} records")

    # ──────────────────────────────────────
    # Create indexes
    # ──────────────────────────────────────
    users_collection.create_index("email", unique=True)
    slots_collection.create_index([("location", 1), ("floor", 1)])
    bookings_collection.create_index("user_id")
    payments_collection.create_index("booking_id")

    # ──────────────────────────────────────
    # OTP TTL Index (auto delete after 10 min)
    # ──────────────────────────────────────
    indexes = otps_collection.index_information()

    if "createdAt_1" not in indexes:
        otps_collection.create_index(
            "createdAt",
            expireAfterSeconds=600  # 10 minutes
        )
        print("✅ OTP TTL index created (10 minutes)")

    print(f"🚀 MongoDB initialized — DB: {DB_NAME}")