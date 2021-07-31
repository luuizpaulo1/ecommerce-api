from datetime import datetime
from uuid import uuid4 as uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.api.models.base import BaseModel
from db import db


class OrderModel(BaseModel):
    __tablename__ = 'orders'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid)
    client_id = db.Column(UUID(as_uuid=True), ForeignKey('clients.id'))
    status = db.Column(db.String(50))  # WAITING_PAYMENT, PAID, REFUNDED, REFUSED, CANCELLED
    total_amount = db.Column(db.Integer)
    products = db.Column(JSONB)

    @classmethod
    def get_order_by_id(cls, order_id):
        order = cls.query.filter_by(
            id=order_id,
            deleted=False
        ).first()
        if order:
            return order
        return None

    def save_order(self):
        db.session.add(self)
        db.session.commit()

    def add_products(self, products_to_be_added: dict):
        """
        products_to_be_added:
        {'APPLE':
            {
                'quantity': 1,
                'name': 'Apple',
                'description': 'Delicious Apple',
                'unit_price': 100
            }
        }
        """

        from ..utils import lod_to_dict, dict_to_lod

        order_products = lod_to_dict(self.products)
        order_products_ids = [product_id for product_id in order_products]
        for product_id in products_to_be_added:
            if product_id in order_products_ids:
                old_product = order_products[product_id]
                new_quantity = old_product['quantity'] + products_to_be_added[product_id]['quantity']
                new_amount = products_to_be_added[product_id]['unit_price'] * new_quantity
                new_unit_price = products_to_be_added[product_id]['unit_price']
                new_product = old_product.copy()
                new_product['quantity'] = new_quantity
                new_product['amount'] = new_amount
                new_product['unit_price'] = new_unit_price
                order_products[product_id] = new_product
            else:
                new_product = {
                    'name': products_to_be_added[product_id]['name'],
                    'description': products_to_be_added[product_id]['description'],
                    'unit_price': products_to_be_added[product_id]['unit_price'],
                    'quantity': products_to_be_added[product_id]['quantity'],
                    'amount': products_to_be_added[product_id]['unit_price'] * products_to_be_added[product_id][
                        'quantity']
                }
                order_products[product_id] = new_product
        order_products = dict_to_lod(order_products)
        self.total_amount = sum([product['amount'] for product in order_products])
        self.updated_at = datetime.utcnow()
        self.products = order_products

    def remove_products(self, products_to_be_removed: dict):
        """
        products_to_be_removed:
        {'APPLE':
            {
                'quantity': 1,
                'name': 'Apple',
                'description': 'Delicious Apple',
                'unit_price': 100
            }
        }
        """
        from ..utils import lod_to_dict, dict_to_lod

        order_products = lod_to_dict(self.products)

        # if all of the requested products to be removed are already in the order
        for product_id in products_to_be_removed:
            removing_quantity = products_to_be_removed[product_id]['quantity']
            if removing_quantity < order_products[product_id]['quantity']:
                order_products[product_id]['quantity'] -= removing_quantity
                order_products[product_id]['amount'] -= products_to_be_removed[product_id][
                                                            'unit_price'] * removing_quantity
            elif removing_quantity >= order_products[product_id]['quantity']:
                order_products.pop(product_id)
        order_products = dict_to_lod(order_products)
        self.total_amount = sum([product['amount'] for product in order_products])
        self.updated_at = datetime.utcnow()
        self.products = order_products

    def cancel(self):
        self.status = 'CANCELLED'
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': str(self.id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'client_id': str(self.client_id),
            'status': self.status,
            'total_amount': self.total_amount,
            'products': self.products
        }
