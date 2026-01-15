from flask import make_response, request, session
from flask_restful import Resource
import datetime
from config import app, db, api
from models import User, Service, Category, Booking

# ==========================================
# Home Resource
# ==========================================
class Home(Resource):
    """
    Resource for the root endpoint. 
    Used to verify the API is running.
    """
    def get(self):
        # Return a welcome message
        return make_response({"message": "Welcome to LocalLink API"}, 200)

# ==========================================
# Services Resource
# ==========================================
class Services(Resource):
    """
    Resource for handling general Service operations.
    """
    def get(self):
        """
        Fetch all available services from the database.
        """
        # Query all services and convert to dictionary format
        services = [s.to_dict() for s in Service.query.all()]
        # Return list of services
        return make_response(services, 200)

    def post(self):
        """
        Create a new service.
        Expects title, description, price, provider_id, and category_id in JSON payload.
        """
        data = request.get_json()
        try:
            # Create new Service instance
            new_service = Service(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                image_url=data.get('image_url'),
                provider_id=data['provider_id'],
                category_id=data['category_id']
            )
            # Add to session and commit to database
            db.session.add(new_service)
            db.session.commit()
            # Return new service data
            return make_response(new_service.to_dict(), 201)
        except Exception as e:
            # Handle any errors during creation
            return make_response({"error": str(e)}, 400)

# ==========================================
# ServiceByID Resource
# ==========================================
class ServiceByID(Resource):
    """
    Resource for handling operations on a specific service by ID.
    """
    def get(self, id):
        """
        Fetch a single service by its ID.
        """
        service = Service.query.filter_by(id=id).first()
        if not service:
            return make_response({"error": "Service not found"}, 404)
        return make_response(service.to_dict(), 200)

    def patch(self, id):
        """
        Update specific fields of a service.
        """
        service = Service.query.filter_by(id=id).first()
        if not service:
            return make_response({"error": "Service not found"}, 404)
        
        data = request.get_json()
        # Update attributes dynamically
        for attr in data:
            setattr(service, attr, data[attr])
        
        db.session.commit()
        return make_response(service.to_dict(), 200)

    def delete(self, id):
        """
        Delete a service from the database.
        """
        service = Service.query.filter_by(id=id).first()
        if not service:
            return make_response({"error": "Service not found"}, 404)
        
        db.session.delete(service)
        db.session.commit()
        return make_response({}, 204)

# ==========================================
# Categories Resource
# ==========================================
class Categories(Resource):
    """
    Resource for general Category operations.
    """
    def get(self):
        """
        List all service categories.
        """
        categories = [c.to_dict() for c in Category.query.all()]
        return make_response(categories, 200)

    def post(self):
        """
        Create a new category.
        """
        data = request.get_json()
        try:
            new_cat = Category(
                name=data['name'],
                image_url=data.get('image_url')
            )
            db.session.add(new_cat)
            db.session.commit()
            return make_response(new_cat.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

# ==========================================
# CategoryByID Resource
# ==========================================
class CategoryByID(Resource):
    """
    Resource for operations on a specific Category.
    """
    def get(self, id):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return make_response({"error": "Category not found"}, 404)
        return make_response(category.to_dict(), 200)

    def patch(self, id):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return make_response({"error": "Category not found"}, 404)
        
        data = request.get_json()
        for attr in data:
            setattr(category, attr, data[attr])
        
        db.session.commit()
        return make_response(category.to_dict(), 200)

    def delete(self, id):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return make_response({"error": "Category not found"}, 404)
        
        db.session.delete(category)
        db.session.commit()
        return make_response({}, 204)

# ==========================================
# Bookings Resource
# ==========================================
class Bookings(Resource):
    """
    Resource for handling bookings.
    """
    def get(self):
        """
        List all bookings.
        """
        bookings = [b.to_dict() for b in Booking.query.all()]
        return make_response(bookings, 200)

    def post(self):
        """
        Create a new booking.
        Parses date string to datetime object.
        """
        data = request.get_json()
        try:
            # Parse date string to python datetime object
            booking_date = datetime.datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            
            new_booking = Booking(
                service_id=data['service_id'],
                client_id=data['client_id'],
                date=booking_date,
                notes=data.get('notes'),
                location=data['location'],
                contact_phone=data['contact_phone']
            )
            db.session.add(new_booking)
            db.session.commit()
            return make_response(new_booking.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

class BookingByID(Resource):
    """
    Resource for handling operations on a specific booking by ID.
    """
    def patch(self, id):
        """
        Update booking status.
        """
        booking = Booking.query.filter_by(id=id).first()
        if not booking:
            return make_response({"error": "Booking not found"}, 404)
        
        data = request.get_json()
        if 'status' in data:
            booking.status = data['status']
            db.session.commit()
            return make_response(booking.to_dict(), 200)
        
        return make_response({"error": "No status provided"}, 400)

    def delete(self, id):
        """
        Delete a booking.
        """
        booking = Booking.query.filter_by(id=id).first()
        if not booking:
            return make_response({"error": "Booking not found"}, 404)
        
        db.session.delete(booking)
        db.session.commit()
        return make_response({}, 204)

# ==========================================
# Users Resource
# ==========================================
class Users(Resource):
    """
    Resource for User management.
    """
    def get(self):
        """
        List all users (Testing only).
        """
        users = [u.to_dict() for u in User.query.all()]
        return make_response(users, 200)

    def post(self):
        """
        Register a new user.
        """
        data = request.get_json()
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                role=data['role'],
                image_url=data.get('image_url')
            )
            # Use property setter for password hashing
            user.password_hash = data['password']
            
            db.session.add(user)
            db.session.commit()
            return make_response(user.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

# ==========================================
# Register Resources
# ==========================================
api.add_resource(Home, '/')
api.add_resource(Services, '/services')
api.add_resource(ServiceByID, '/services/<int:id>')
api.add_resource(Categories, '/categories')
api.add_resource(CategoryByID, '/categories/<int:id>')
api.add_resource(Bookings, '/bookings')
api.add_resource(BookingByID, '/bookings/<int:id>')
api.add_resource(Users, '/users')

# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)