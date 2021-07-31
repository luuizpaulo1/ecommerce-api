from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..models import ProductModel
from app.resources.authentication import requires_auth


class ProductController(Resource):

    @staticmethod
    @requires_auth
    def get(product_id):
        product = ProductModel.get_product_by_id(product_id)
        if product:
            return product.json(), 200
        return {'msg': 'Product not found'}, 404

    @staticmethod
    @requires_auth
    def post():
        required_args = ['id', 'name', 'unit_price']
        accepted_args = ['id', 'name', 'description', 'unit_price']

        product_data = {key: value for key, value in request.json.items() if key in accepted_args}

        for key in required_args:
            if key not in product_data.keys():
                return {'msg': f'The field \'{key}\' is required'}, 400

        try:
            new_product = ProductModel(**product_data)
            new_product.save_product()
            return new_product.json(), 201
        except IntegrityError:
            return {'msg': f'Product ID \'{product_data["id"]}\' already exists'}, 400

    @staticmethod
    @requires_auth
    def put():
        required_args = ['id']
        accepted_args = ['id', 'name', 'description', 'unit_price']

        product_data = {key: value for key, value in request.json.items() if key in accepted_args}

        for key in required_args:
            if key not in product_data.keys():
                return {'msg': f'The field \'{key}\' is required'}, 400

        product = ProductModel.get_product_by_id(product_data['id'])

        if product:
            product.update(**product_data)
            return product.json(), 201

        return {'msg': 'Product not found'}, 404

    @staticmethod
    @requires_auth
    def delete(product_id):
        product = ProductModel.get_product_by_id(product_id)
        if product:
            product.delete()
            return None, 204
        else:
            return {'msg': f'Product ID \'{product_id}\' not found'}, 404
