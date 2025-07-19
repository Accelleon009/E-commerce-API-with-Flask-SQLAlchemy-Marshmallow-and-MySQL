from flask import Blueprint, request, jsonify
from models import Product, db
from schemas import ProductSchema
from flask_jwt_extended import jwt_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products))

@products_bp.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(product))

@products_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    product_name = request.json['product_name']
    existing_product = Product.query.filter_by(product_name=product_name).first()
    
    if existing_product:
        return jsonify({"error": "Product with this name already exists"}), 400
    
    new_product = Product(
        product_name=product_name,
        price=request.json['price']
    )
    db.session.add(new_product)
    db.session.commit()
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(new_product)), 201

@products_bp.route('/products/<id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    product.product_name = request.json.get('product_name', product.product_name)
    product.price = request.json.get('price', product.price)
    db.session.commit()
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(product))

@products_bp.route('/products/<id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})