import os
from functools import wraps

from flask import Blueprint
from flask import request
from flask_restful import Api

from .controllers import ClientController, OrderController, ProductController

def setup_blueprint():
    bp = Blueprint("api", __name__, url_prefix="/")
    api = Api(bp)

    api.add_resource(ClientController,
                     '/client',
                     '/client/<client_id>',
                     '/client/<client_id>/orders')

    api.add_resource(OrderController,
                     '/order',
                     '/order/<order_id>',
                     '/order/<order_id>/products',
                     '/order/cancel',
                     '/order/add_products',
                     '/order/remove_products')

    api.add_resource(ProductController,
                     '/product',
                     '/product/<product_id>')

    return bp
