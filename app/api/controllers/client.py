from datetime import datetime

from flask import request
from flask_restful import Resource

from ..models import ClientModel
from app.resources.authentication import requires_auth


class ClientController(Resource):
    @staticmethod
    @requires_auth
    def get(client_id):
        url_rule = str(request.url_rule)
        if url_rule == '//client/<client_id>':
            client = ClientModel.get_client_by_id(client_id)
            if client:
                return client.json()
            return {'msg': 'Client not found'}, 404
        elif 'orders' in url_rule:
            client = ClientModel.get_client_by_id(client_id)
            client_orders = [order.json() for order in client.orders]
            return client_orders, 201

    @staticmethod
    @requires_auth
    def post():
        required_args = ['name', 'birth_date', 'document']
        accepted_args = ['name', 'birth_date', 'document']
        client_data = {key: value for key, value in request.json.items() if key in accepted_args}

        for key in required_args:
            if key not in client_data.keys():
                return {'msg': f'\'{key}\' field is required'}, 400

        try:
            client_data['birth_date'] = datetime.strptime(client_data['birth_date'], '%Y-%m-%d')
        except ValueError:
            return {'msg': 'birth_date date format should be \'YYYY-MM-DD\''}

        new_client = ClientModel(**client_data)
        new_client.save_client()
        return new_client.json(), 201

    @staticmethod
    @requires_auth
    def put():
        required_args = ['id']
        accepted_args = ['id', 'name', 'birth_date', 'document']

        client_data = {key: value for key, value in request.json.items() if key in accepted_args}

        for key in required_args:
            if key not in client_data.keys():
                return {'msg': f'The field \'{key}\' is required'}, 400

        client = ClientModel.get_client_by_id(client_data['id'])

        if client:
            client.update(**client_data)
            return client.json(), 201

        return {'msg': 'Client not found'}, 404

    @staticmethod
    @requires_auth
    def delete(client_id):
        client = ClientModel.get_client_by_id(client_id)
        if client:
            client.delete()
            return None, 204
        else:
            return {'msg': f'Client ID \'{client_id}\' not found'}, 404
