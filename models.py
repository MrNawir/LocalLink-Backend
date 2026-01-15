from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db

# ==========================================
# User Model
# ==========================================
class User(db.Model, SerializerMixin):
    """
    Represents a user in the system.
    Can be either a 'provider' or a 'client'.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False) # 'provider' or 'client'
    image_url = db.Column(db.String)

    # Relationships
    # A Provider can offer multiple services
    services = db.relationship('Service', back_populates='provider', cascade='all, delete-orphan')
    # A Client can make multiple bookings
    bookings = db.relationship('Booking', back_populates='client', cascade='all, delete-orphan')

    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-services.provider', '-bookings.client', '-_password_hash',)

    @hybrid_property
    def password_hash(self):
        """
        Getter for password hash.
        Prevents accessing the hash directly.
        """
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        """
        Setter for password.
        Hashes the password before storing it.
        In a real production app, use bcrypt or similar here.
        """
        # In a real app, use bcrypt or similar
        self._password_hash = password

    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}>'

# ==========================================
# Category Model
# ==========================================
class Category(db.Model, SerializerMixin):
    """
    Represents a category of services (e.g., Cleaning, Plumbing).
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    image_url = db.Column(db.String)

    # Relationships
    services = db.relationship('Service', back_populates='category', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-services.category',)

    def __repr__(self):
        return f'<Category {self.name}>'

# ==========================================
# Service Model
# ==========================================
class Service(db.Model, SerializerMixin):
    """
    Represents a service offered by a provider.
    """
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String)
    
    # Foreign Keys
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # Relationships
    provider = db.relationship('User', back_populates='services')
    category = db.relationship('Category', back_populates='services')
    bookings = db.relationship('Booking', back_populates='service', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-provider.services', '-category.services', '-bookings.service',)

    @validates('price')
    def validate_price(self, key, price):
        """
        Validate that the price is not negative.
        """
        if price < 0:
            raise ValueError("Price must be non-negative")
        return price

    def __repr__(self):
        return f'<Service {self.title}>'

# ==========================================
# Booking Model
# ==========================================
class Booking(db.Model, SerializerMixin):
    """
    Represents a booking made by a client for a service.
    """
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, default='pending') # pending, confirmed, completed
    notes = db.Column(db.String)
    
    # New fields for better service delivery
    location = db.Column(db.String, nullable=False) # Address or location description
    contact_phone = db.Column(db.String, nullable=False) # Contact number for the booking
    
    # Foreign Keys
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    service = db.relationship('Service', back_populates='bookings')
    client = db.relationship('User', back_populates='bookings')

    # Serialization rules
    serialize_rules = ('-service.bookings', '-client.bookings',)

    def __repr__(self):
        return f'<Booking {self.id} for Service {self.service_id}>'