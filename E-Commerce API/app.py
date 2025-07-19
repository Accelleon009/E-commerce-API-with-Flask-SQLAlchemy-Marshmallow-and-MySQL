from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os
import logging
from config import Config
from models import db, User  # Import User model
from schemas import ma
from routes.users import users_bp
from routes.products import products_bp
from routes.orders import orders_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize extensions
db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    logger.info('Headers: %s', request.headers)
    logger.info('Body: %s', request.get_data())

# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

# Drop and Create Database Tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    user_id_str = str(user.id)
    app.logger.info(f"User ID (string): {user_id_str} (type: {type(user_id_str)})")
    
    access_token = create_access_token(identity=user_id_str)  # Convert user ID to string
    return jsonify(access_token=access_token)

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e)
    }
    return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)