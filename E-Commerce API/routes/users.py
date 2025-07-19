from flask import Blueprint, request, jsonify
from models import User, db
from schemas import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users))

@users_bp.route('/users/<id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))

@users_bp.route('/users', methods=['POST'])
def add_user():
    email = request.json['email']
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400
    
    new_user = User(
        name=request.json['name'],
        address=request.json['address'],
        email=email,
        password_hash=generate_password_hash(request.json['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    user_schema = UserSchema()
    return jsonify(user_schema.dump(new_user)), 201

@users_bp.route('/users/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    
    if 'name' in request.json:
        user.name = request.json['name']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        user.email = request.json['email']
    
    db.session.commit()
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))

@users_bp.route('/users/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})