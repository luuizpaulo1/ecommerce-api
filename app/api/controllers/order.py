from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..models import OrderModel, ProductModel
from app.resources.authentication import requires_auth


class OrderController(Resource):

    @staticmethod
    @requires_auth
    def get(order_id):
        url_rule = str(request.url_rule)
        order = OrderModel.get_order_by_id(order_id)
        if order:
            if url_rule == '//order/<order_id>':
                return order.json(), 200
            elif 'products' in url_rule:
                return order.products, 200
        return {'msg': f'Order ID \'{order_id}\' not found'}, 404

    @staticmethod
    @requires_auth
    def post():
        from ..utils import lod_to_dict, dict_to_lod
        url_rule = str(request.url_rule)

        # create order
        if url_rule == '//order':
            required_args = ['client_id', 'status', 'products']
            accepted_args = ['client_id', 'status', 'products']

            # filter only accepted args
            order_data = {key: value for key, value in request.json.items() if key in accepted_args}

            # check required args
            for key in required_args:
                if key not in order_data.keys():
                    return {'msg': f'The \'{key}\' field is required'}, 400

            # formatting requested products
            requested_products = lod_to_dict(order_data['products'])

            # formatting requested products data
            requested_products_data = ProductModel.query.filter(
                ProductModel.id.in_(requested_products.keys())
            ).all()
            requested_products_data = [product.json() for product in requested_products_data]
            requested_products_data = lod_to_dict(requested_products_data)

            # if all of the requested products exist
            if len(requested_products_data) == len(requested_products):
                products_to_be_added = dict()
                for product_id in requested_products:
                    products_to_be_added[product_id] = requested_products[product_id]
                    products_to_be_added[product_id].update(requested_products_data[product_id])

                    quantity = products_to_be_added[product_id]['quantity']
                    unit_price = products_to_be_added[product_id]['unit_price']

                    products_to_be_added[product_id]['amount'] = quantity * unit_price

                products_to_be_added = dict_to_lod(products_to_be_added)
                order_data['products'] = products_to_be_added
                order = OrderModel(**order_data)
                try:
                    order.save_order()
                    return order.json(), 201
                except IntegrityError:
                    order.rollback()
                    return {'msg': f'Client ID \'{order_data["client_id"]}\' not found'}, 404
            # if at least one of the requested products do not exist
            else:
                requested_product_ids = [key for key in requested_products.keys()]
                requested_product_ids_that_exist = [product.id for product in requested_products_data]
                for product_id in requested_product_ids:
                    if product_id not in requested_product_ids_that_exist:
                        return {'msg': f'Product ID \'{product_id}\' not found'}, 404

        # add products to an existing order
        elif 'add_products' in url_rule:
            required_args = ['order_id', 'products']
            accepted_args = ['order_id', 'products']

            # filter only accepted args
            order_data = {key: value for key, value in request.json.items() if key in accepted_args}

            # check required args
            for key in required_args:
                if key not in order_data.keys():
                    return {'msg': f'The \'{key}\' field is required'}, 400

            # formatting requested products
            requested_products = lod_to_dict(order_data['products'])
            # formatting requested products data
            requested_products_data = ProductModel.query.filter(
                ProductModel.id.in_(requested_products.keys())
            ).all()
            requested_products_data = [product.json() for product in requested_products_data]
            requested_products_data = lod_to_dict(requested_products_data)

            # if all of the requested products exist
            if len(requested_products_data) == len(requested_products):
                products_to_be_added = dict()
                for product_id in requested_products:
                    products_to_be_added[product_id] = requested_products[product_id]
                    products_to_be_added[product_id].update(requested_products_data[product_id])
                print(f'{products_to_be_added=}')
                order = OrderModel.get_order_by_id(order_data['order_id'])
                if order:
                    order.add_products(products_to_be_added)
                    order.save_order()
                    return order.json(), 201
                else:
                    return {'msg': f'Order ID \'{order_data["order_id"]}\' not found'}, 404

            # if at least one of the requested products do not exist
            else:
                requested_product_ids = [key for key in requested_products.keys()]
                requested_product_ids_that_exist = [product.id for product in requested_products_data]
                for product_id in requested_product_ids:
                    if product_id not in requested_product_ids_that_exist:
                        return {'msg': f'Product ID {product_id} not found'}, 404

        # remove products from existing order
        elif 'remove_products' in url_rule:
            required_args = ['order_id', 'products']
            accepted_args = ['order_id', 'products']

            # filter only accepted args
            order_data = {key: value for key, value in request.json.items() if key in accepted_args}

            # check required args
            for key in required_args:
                if key not in order_data.keys():
                    return {'msg': f'The \'{key}\' field is required'}, 400

            # formatting requested products
            requested_products = lod_to_dict(order_data['products'])

            # formatting requested products data
            requested_products_data = ProductModel.query.filter(
                ProductModel.id.in_(requested_products.keys())
            ).all()
            requested_products_data = [product.json() for product in requested_products_data]
            requested_products_data = lod_to_dict(requested_products_data)

            # if all of the requested products exist
            if len(requested_products_data) == len(requested_products):
                products_to_be_removed = dict()
                for product_id in requested_products:
                    products_to_be_removed[product_id] = requested_products[product_id]
                    products_to_be_removed[product_id].update(requested_products_data[product_id])
                order = OrderModel.get_order_by_id(order_data['order_id'])
                if order:
                    order_products = lod_to_dict(order.products)
                    order_products_ids = [product_id for product_id in order_products]
                    if all([product_id in order_products_ids for product_id in products_to_be_removed]):
                        order.remove_products(products_to_be_removed)
                        order.save_order()
                        return order.json(), 201
                    else:
                        for product_id in products_to_be_removed:
                            if product_id not in order_products:
                                return {'msg': f'Product ID \'{product_id}\' does not belong to the specified order'}, 400
                return {'msg': f'Order ID \'{order_data["order_id"]}\' not found'}, 404

            # if at least one of the requested products do not exist
            else:
                requested_product_ids = [key for key in requested_products.keys()]
                requested_product_ids_that_exist = [product.id for product in requested_products_data]
                for product_id in requested_product_ids:
                    if product_id not in requested_product_ids_that_exist:
                        return {'msg': f'Product ID {product_id} not found'}, 404

        # cancel the order
        elif 'cancel' in url_rule:
            required_args = ['id']
            accepted_args = ['id']

            # filter only accepted args
            order_data = {key: value for key, value in request.json.items() if key in accepted_args}

            # check required args
            for key in required_args:
                if key not in order_data.keys():
                    return {'msg': f'The \'{key}\' field is required'}, 400

            order = OrderModel.get_order_by_id(order_data['id'])
            if order:
                order.cancel()
                return order.json(), 201
            else:
                return {'msg': f'Order ID \'{order_data["id"]}\' not found'}, 404

    @staticmethod
    @requires_auth
    def put():
        required_args = ['id']
        accepted_args = ['id', 'status']

        order_data = {key: value for key, value in request.json.items() if key in accepted_args}

        for key in required_args:
            if key not in order_data.keys():
                return {'msg': f'The \'{key}\' field is required'}, 400

        accepted_statuses = ['WAITING_PAYMENT', 'PAID', 'REFUNDED', 'REFUSED', 'CANCELLED']
        if order_data['status'] not in accepted_statuses:
            return {'msg': f'Status \'{order_data["status"]}\' is not accepted'}, 400
        order = OrderModel.get_order_by_id(order_data['id'])

        if order:
            order.update(**order_data)
            return order.json(), 201

        return {'msg': f'Order ID \'{order_data["id"]}\' not found'}, 404

    @staticmethod
    @requires_auth
    def delete(order_id):
        order = OrderModel.get_order_by_id(order_id)
        if order:
            order.delete()
            return None, 204
        else:
            return {'msg': f'Order ID \'{order_id}\' not found'}, 404
