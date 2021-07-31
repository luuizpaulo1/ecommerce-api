from datetime import datetime

from db import db


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'id':
                continue
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.deleted = True
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
