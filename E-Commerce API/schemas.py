from flask_marshmallow import Marshmallow
from models import User, Order, Product

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product