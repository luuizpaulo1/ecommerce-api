from app.api.models.base import BaseModel
from db import db


class ProductModel(BaseModel):
    __tablename__ = 'products'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    unit_price = db.Column(db.Integer)

    @classmethod
    def get_product_by_id(cls, product_id):
        product = cls.query.filter_by(
            id=product_id,
            deleted=False
        ).first()
        if product:
            return product
        return None

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'name': self.name,
            'description': self.description,
            'unit_price': self.unit_price
        }
