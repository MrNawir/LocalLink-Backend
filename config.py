from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os

# Define metadata for SQLAlchemy
# naming_convention is used to ensure consistent constraints naming in migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Instantiate SQLAlchemy with the custom metadata
db = SQLAlchemy(metadata=metadata)

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
# Uses 'DATABASE_URI' from environment variables, defaults to local sqlite app.db if not found
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')

# Disable modification tracking to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JSON output to not be compacted (for readability during dev)
app.json.compact = False

# Initialize Flask-Migrate for handling database schema changes
migrate = Migrate(app, db)

# Initialize the database with the app context
db.init_app(app)

# Initialize RESTful API
api = Api(app)

# Enable Cross-Origin Resource Sharing (CORS) for front-end communication
CORS(app)