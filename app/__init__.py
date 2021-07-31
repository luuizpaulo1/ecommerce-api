import os

from flask import Flask

from app.api.models import *
from db import db


def mock_data(app):
    with app.app_context():
        mock_client = {
            'id': '276b6688-d835-47eb-ab53-4db79727a0c1',
            'name': 'Geralt of Rivia',
            'birth_date': '1151-10-19',
            'document': '12345678910'
        }
        new_client = ClientModel(**mock_client)
        new_client.save_client()

        mock_product = {
            'id': 'SIHIL',
            'name': 'Sihil',
            'description': 'Magic sword forged in Mahakam.',
            'unit_price': '214500'
        }
        new_product = ProductModel(**mock_product)
        new_product.save_product()

        mock_order = {
            'id': '531dc18b-7525-49aa-b00b-aaa43bb63282',
            'client_id': '276b6688-d835-47eb-ab53-4db79727a0c1',
            'status': 'WAITING_PAYMENT',
            'products': [
                {
                    'id': 'SIHIL',
                    'quantity': 1
                }
            ]
        }
        new_order = OrderModel(**mock_order)
        new_order.save_order()


def make_app(testing=False):
    from .api import setup_blueprint as blueprint

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', default='5432')
    db_database = os.getenv('DB_DATABASE')
    print(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}')

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/test'
        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()
            mock_data(app)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
        db.init_app(app)

    app.register_blueprint(blueprint())

    return app
