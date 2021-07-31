from uuid import uuid4 as uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.api.models.base import BaseModel
from db import db


class ClientModel(BaseModel):
    __tablename__ = 'clients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid)
    name = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    document = db.Column(db.String(14))
    orders = relationship("OrderModel", backref='owner')

    @classmethod
    def get_client_by_id(cls, client_id):
        client = cls.query.filter_by(
            id=client_id,
            deleted=False
        ).first()
        if client:
            return client
        return None

    def save_client(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': str(self.id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'name': self.name,
            'birth_date': str(self.birth_date),
            'document': self.document
        }
