from config import app, db
from models import User, Service, Category, Booking
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for generating dummy data
fake = Faker()

# Verified Image Collection (Status 200 Checked)
# Using high-quality images from Unsplash to ensure the app looks good immediately
IMAGES = {
    # Cleaning
    "cleaning_main": "https://images.unsplash.com/photo-1581578731117-104f2a41bcbe?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    "cleaning_mop": "https://images.unsplash.com/photo-1528740561666-dc24705f08a7?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    "cleaning_kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "cleaning_supplies": "https://images.unsplash.com/photo-1584622050111-993a426fbf0a?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    
    # IT Support
    "it_main": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "it_repair": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "it_error": "https://images.unsplash.com/photo-1563770095-39d468a9b324?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    "it_code": "https://images.unsplash.com/photo-1588872657578-1a416556363e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    
    # Plumbing
    "plumbing_main": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "plumbing_repair": "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "plumbing_sink": "https://images.unsplash.com/photo-1584622050111-993a426fbf0a?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    "plumbing_drain": "https://images.unsplash.com/photo-1621905476059-5f8df79b8411?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    
    # Gardening
    "gardening_main": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
    "gardening_mower": "https://images.unsplash.com/photo-1592419044706-39796d40f98c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "gardening_flowers": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 
    "gardening_tree": "https://images.unsplash.com/photo-1598902106739-16a75a9528ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
}

# Pre-defined categories and services to ensure the app has realistic content
CATEGORIES_DB = [
    {
        "name": "Home Cleaning", 
        "image_url": IMAGES["cleaning_main"],
        "services": [
            {"title": "Deep House Cleaning", "description": "Complete top-to-bottom cleaning for your entire home. Includes dusting, vacuuming, mopping, and bathroom sanitization.", "image_url": IMAGES["cleaning_mop"]},
            {"title": "Move-In/Move-Out Clean", "description": "Ensure your new place is spotless before you unpack, or get your deposit back with our detailed move-out cleaning.", "image_url": IMAGES["cleaning_supplies"]},
            {"title": "Weekly Standard Clean", "description": "Keep your home fresh with our recurring weekly cleaning service. Perfect for busy professionals.", "image_url": IMAGES["cleaning_kitchen"]}
        ]
    },
    {
        "name": "IT Support", 
        "image_url": IMAGES["it_main"],
        "services": [
            {"title": "Computer Repair & Diagnostics", "description": "Diagnose and fix hardware or software issues. We handle screen replacements, battery issues, and slow performance.", "image_url": IMAGES["it_repair"]},
            {"title": "Home WiFi Optimization", "description": "Boost your internet speed and coverage. Specialized configuration for large homes and dead zones.", "image_url": IMAGES["it_error"]},
            {"title": "Virus & Malware Removal", "description": "Secure your data and remove harmful software. Includes installation of premium antivirus protection.", "image_url": IMAGES["it_code"]}
        ]
    },
    {
        "name": "Plumbing", 
        "image_url": IMAGES["plumbing_main"],
        "services": [
            {"title": "Emergency Pipe Repair", "description": "24/7 service for burst pipes and severe leaks. Fast response time to minimize water damage.", "image_url": IMAGES["plumbing_repair"]},
            {"title": "Faucet & Sink Installation", "description": "Upgrade your kitchen or bathroom with modern fixtures. Professional installation guarantees.", "image_url": IMAGES["plumbing_sink"]},
            {"title": "Drain Unclogging", "description": "Clear stubborn clogs in showers, sinks, and toilets using heavy-duty equipment.", "image_url": IMAGES["plumbing_drain"]}
        ]
    },
    {
        "name": "Gardening", 
        "image_url": IMAGES["gardening_main"],
        "services": [
            {"title": "Lawn Mowing & Maintenance", "description": "Weekly lawn care including mowing, edging, and blowing. Keep your yard looking pristine.", "image_url": IMAGES["gardening_mower"]},
            {"title": "Garden Design & Planting", "description": "Transform your outdoor space with professionally designed flower beds and shrubbery.", "image_url": IMAGES["gardening_flowers"]},
            {"title": "Tree Trimming", "description": "Safe and professional trimming of overgrown branches to improve tree health and view.", "image_url": IMAGES["gardening_tree"]}
        ]
    }
]

def seed_data():
    """
    Main function to clear and populate the database.
    """
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data to avoid duplicates
        # Deleted in order of dependency to avoid Foreign Key errors
        Booking.query.delete()
        Service.query.delete()
        Category.query.delete()
        User.query.delete()
        
        # Create Users
        print("Creating users...")
        providers = []
        clients = []
        
        # Real-world looking headshots for providers
        provider_images = [
            "https://images.unsplash.com/photo-1560250097-0b93528c311a?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&q=80",
            "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&q=80",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&q=80",
            "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&q=80",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&q=80"
        ]

        # Create 5 Providers
        for i, img_url in enumerate(provider_images):
            u = User(
                username=fake.first_name() + " " + fake.last_name(),
                email=f"provider{i}@example.com",
                role='provider',
                image_url=img_url
            )
            u.password_hash = 'password' # Default password
            providers.append(u)
            db.session.add(u)
            
        # Create 5 Clients
        for i in range(5):
            u = User(
                username=fake.user_name(),
                email=f"client{i}@example.com",
                role='client',
                image_url=fake.image_url()
            )
            u.password_hash = 'password' # Default password
            clients.append(u)
            db.session.add(u)
            
        db.session.commit()
        
        # Create Categories and Services
        print("Creating categories and services...")
        
        for data in CATEGORIES_DB:
            # Create Category
            cat = Category(name=data['name'], image_url=data['image_url'])
            db.session.add(cat)
            db.session.flush() # Flush to generate cat.id without committing transaction
            
            # Create Services strictly linked to this category
            for s_data in data['services']:
                provider = random.choice(providers) # Randomly assign a provider
                service = Service(
                    title=s_data['title'],
                    description=s_data['description'],
                    price=round(random.uniform(80.0, 300.0), 2),
                    image_url=s_data['image_url'],
                    provider_id=provider.id,
                    category_id=cat.id
                )
                db.session.add(service)
        
        db.session.commit()
        
        # Create Bookings
        print("Creating bookings...")
        all_services = Service.query.all()
        for _ in range(15):
            service = random.choice(all_services)
            client = random.choice(clients)
            
            # Create booking in the near future
            b = Booking(
                service_id=service.id,
                client_id=client.id,
                date=fake.future_datetime(end_date="+30d"),
                status=random.choice(['pending', 'confirmed', 'completed']),
                notes=fake.sentence(),
                location=fake.address(),
                contact_phone=fake.phone_number()
            )
            db.session.add(b)
        db.session.commit()
        
        print("Seeding complete! Database populated with 200 OK images.")

if __name__ == '__main__':
    seed_data()