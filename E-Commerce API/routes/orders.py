from flask import Blueprint, request, jsonify
from models import Order, Product, User, db
from schemas import OrderSchema, ProductSchema
from utils import validate_date
from flask_jwt_extended import jwt_required

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    order_date = validate_date(request.json['order_date'])
    if not order_date:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"}), 400
    
    user_id = request.json['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    new_order = Order(
        order_date=order_date,
        user_id=user_id
    )
    db.session.add(new_order)
    db.session.commit()
    order_schema = OrderSchema()
    return jsonify(order_schema.dump(new_order)), 201

@orders_bp.route('/orders/<order_id>/add_product/<product_id>', methods=['PUT'])
@jwt_required()
def add_product_to_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    if product in order.products:
        return jsonify({'message': 'Product already in order'}), 400
    order.products.append(product)
    db.session.commit()
    return jsonify({'message': 'Product added to order successfully'})

@orders_bp.route('/orders/<order_id>/remove_product/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_product_from_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    if product not in order.products:
        return jsonify({'message': 'Product not in order'}), 400
    order.products.remove(product)
    db.session.commit()
    return jsonify({'message': 'Product removed from order successfully'})

@orders_bp.route('/orders/user/<user_id>', methods=['GET'])
@jwt_required()
def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    order_schema = OrderSchema(many=True)
    return jsonify(order_schema.dump(orders))

@orders_bp.route('/orders/<order_id>/products', methods=['GET'])
@jwt_required()
def get_products_in_order(order_id):
    order = Order.query.get_or_404(order_id)
    products = order.products
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products))