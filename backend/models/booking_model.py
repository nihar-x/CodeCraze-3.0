from datetime import datetime
from config.db import bookings_collection, slots_collection
from bson import ObjectId


def create_booking(
    user_id,
    slot_id,
    full_name,
    vehicle,
    location,
    floor,
    date,
    time,
    duration,
    total,
    user_email="",
    data={},
):
    """Insert a new booking and mark the slot as occupied. Returns the booking id."""
    booking = {
        "user_id": user_id,
        "user_email": user_email.lower().strip() if user_email else "",
        "slot_id": slot_id,
        "full_name": full_name,
        "vehicle": vehicle,  # Simplified vehicle string for legacy
        "vehicle_details": data.get("vehicle_details", {}),  # Detailed info
        "owner_details": {
            "name": full_name,
            "email": user_email,
            "phone": data.get("phone", ""),
        },
        "location": location,
        "floor": floor,
        "date": date,
        "time": time,
        "duration": float(duration),
        "total": float(total),
        "payment_details": data.get(
            "payment_details",
            {
                "method": "online",
                "status": "paid",
                "transaction_id": f"pay_{ObjectId()}",
            },
        ),
        "status": "active",
        "entry_time": datetime.utcnow().isoformat(),
        "exit_time": None,
        "created_at": datetime.utcnow().isoformat(),
    }

    result = bookings_collection.insert_one(booking)

    # Mark the slot as occupied
    try:
        slots_collection.update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": {"status": "occupied"}},
        )
    except Exception:
        pass  # slot_id might not be a valid ObjectId in some cases

    return str(result.inserted_id)


def get_bookings_by_user(user_id):
    """Return all bookings for a given user by user_id, newest first."""
    bookings = list(
        bookings_collection.find({"user_id": user_id}).sort("created_at", -1)
    )
    for b in bookings:
        b["_id"] = str(b["_id"])
    return bookings


def get_bookings_by_user_email(email):
    """Return all bookings for a user by their email address, newest first."""
    email = email.lower().strip()
    bookings = list(
        bookings_collection.find({"user_email": email}).sort("created_at", -1)
    )
    for b in bookings:
        b["_id"] = str(b["_id"])
    return bookings


def get_all_bookings():
    """Return all bookings, newest first."""
    bookings = list(bookings_collection.find().sort("created_at", -1))
    for b in bookings:
        b["_id"] = str(b["_id"])
    return bookings


def get_booking_by_id(booking_id):
    """Fetch a single booking by its ObjectId."""
    try:
        booking = bookings_collection.find_one({"_id": ObjectId(booking_id)})
        if booking:
            booking["_id"] = str(booking["_id"])
        return booking
    except Exception:
        return None


def cancel_booking_by_id(booking_id):
    """Cancel a booking and free up the parking slot. Returns True on success."""
    try:
        booking = bookings_collection.find_one({"_id": ObjectId(booking_id)})
        if not booking:
            return False

        # Update booking status to cancelled
        bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": "cancelled"}},
        )

        # Free up the associated slot
        slot_id = booking.get("slot_id")
        if slot_id:
            try:
                slots_collection.update_one(
                    {"_id": ObjectId(slot_id)},
                    {"$set": {"status": "available"}},
                )
            except Exception:
                pass  # slot_id might not be a valid ObjectId

        return True
    except Exception:
        return False


def update_booking_status_by_id(booking_id, new_status):
    """Generic status update. Manages slot occupation/availability based on status."""
    try:
        booking = bookings_collection.find_one({"_id": ObjectId(booking_id)})
        if not booking:
            return False

        slot_id = booking.get("slot_id")

        # Define which statuses free up a slot vs occupy it
        FREE_STATUSES = ["completed", "cancelled"]
        OCCUPY_STATUSES = ["active", "confirmed", "paid"]

        update_fields = {"status": new_status}
        if new_status == "completed":
            update_fields["exit_time"] = datetime.utcnow().isoformat()
        elif new_status in OCCUPY_STATUSES:
            update_fields["exit_time"] = None  # Reset if re-activated

        bookings_collection.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": update_fields},
        )

        # Handle Slot State
        if slot_id:
            try:
                new_slot_status = (
                    "available" if new_status in FREE_STATUSES else "occupied"
                )
                slots_collection.update_one(
                    {"_id": ObjectId(slot_id)},
                    {"$set": {"status": new_slot_status}},
                )
            except Exception:
                pass

        return True
    except Exception:
        return False
