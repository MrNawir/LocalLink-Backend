from flask import jsonify, request
from config import app, db
from models import User, Service, Category, Booking
from datetime import datetime

# ==================== ROOT ====================
@app.route("/")
def index():
    return jsonify(message="Welcome to LocalLink API!", status="running")


# ==================== CATEGORIES ====================
@app.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([cat.to_dict() for cat in categories])


@app.route("/categories/<int:id>", methods=["GET"])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())


@app.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    category = Category(
        name=data.get("name"),
        image_url=data.get("image_url")
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@app.route("/categories/<int:id>", methods=["PATCH"])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    if "name" in data:
        category.name = data["name"]
    if "image_url" in data:
        category.image_url = data["image_url"]
    db.session.commit()
    return jsonify(category.to_dict())


@app.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


# ==================== SERVICES ====================
@app.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([svc.to_dict() for svc in services])


@app.route("/services/<int:id>", methods=["GET"])
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify(service.to_dict())


@app.route("/services", methods=["POST"])
def create_service():
    data = request.get_json()
    service = Service(
        title=data.get("title"),
        description=data.get("description"),
        price=float(data.get("price", 0)),
        image_url=data.get("image_url"),
        provider_id=int(data.get("provider_id", 1)),
        category_id=int(data.get("category_id"))
    )
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201


@app.route("/services/<int:id>", methods=["PATCH"])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    if "title" in data:
        service.title = data["title"]
    if "description" in data:
        service.description = data["description"]
    if "price" in data:
        service.price = float(data["price"])
    if "image_url" in data:
        service.image_url = data["image_url"]
    if "category_id" in data:
        service.category_id = int(data["category_id"])
    if "provider_id" in data:
        service.provider_id = int(data["provider_id"])
    db.session.commit()
    return jsonify(service.to_dict())


@app.route("/services/<int:id>", methods=["DELETE"])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted"}), 200


# ==================== BOOKINGS ====================
@app.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings])


@app.route("/bookings/<int:id>", methods=["GET"])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify(booking.to_dict())


@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    try:
        booking = Booking(
            service_id=int(data.get("service_id")),
            client_id=int(data.get("client_id")),
            date=datetime.fromisoformat(data.get("date")),
            status="pending",
            notes=data.get("notes"),
            location=data.get("location"),
            contact_phone=data.get("contact_phone")
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify(booking.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/bookings/<int:id>", methods=["PATCH"])
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    data = request.get_json()
    if "status" in data:
        booking.status = data["status"]
    if "notes" in data:
        booking.notes = data["notes"]
    if "location" in data:
        booking.location = data["location"]
    if "contact_phone" in data:
        booking.contact_phone = data["contact_phone"]
    if "date" in data:
        booking.date = datetime.fromisoformat(data["date"])
    db.session.commit()
    return jsonify(booking.to_dict())


@app.route("/bookings/<int:id>", methods=["DELETE"])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200


# ==================== USERS ====================
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# ==================== RUN ====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
