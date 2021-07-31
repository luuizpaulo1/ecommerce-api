import os


def test_create_user_success(test_client):
    payload = {
        'name': 'Cirilla Fiona Elen Riannon',
        'birth_date': '1253-10-19',
        'document': '12345678911'
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/client'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 201


def test_create_user_fail(test_client):
    payload = {
        'birth_date': '1253-10-19',
        'document': '12345678911'
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/client'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 400
    assert b'is required' in response.data


def test_create_products(test_client):
    payload = {
        "id": "DEIREADH",
        "name": "Deireadh",
        "description": "Tedd Deireadh!",
        "unit_price": 75000
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/product'
    response = test_client.post(url, headers=headers, json=payload)
    print(response.data)
    assert response.status_code == 201


def test_create_order(test_client):
    payload = {
        "client_id": '276b6688-d835-47eb-ab53-4db79727a0c1',
        "status": "WAITING_PAYMENT",
        "products": [
            {
                "id": "SIHIL",
                "quantity": 1
            }
        ]
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/order'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 201


def test_create_order_fail(test_client):
    payload = {
        "client_id": '276b6688-d835-47eb-ab53-4db79727a0c2',
        "status": "WAITING_PAYMENT",
        "products": [
            {
                "id": "SIHIL",
                "quantity": 1
            }
        ]
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/order'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 404


def test_add_items_to_order(test_client):
    payload = {
        "order_id": "531dc18b-7525-49aa-b00b-aaa43bb63282",
        "products": [
            {
                "id": "SIHIL",
                "quantity": 10

            }
        ]
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/order/add_products'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 201
    assert response.json['products'][0]['unit_price'] == 214500
    assert response.json['products'][0]['quantity'] == 11
    assert response.json['products'][0]['amount'] == 214500*11


def test_add_items_to_non_existing_order(test_client):
    payload = {
        "order_id": "531dc18b-7525-49aa-b00b-aaa43bb63212",
        "products": [
            {
                "id": "SIHIL",
                "quantity": 10

            }
        ]
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/order/add_products'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 404
    assert b'not found' in response.data


def test_remove_items_from_order(test_client):
    payload = {
        "order_id": "531dc18b-7525-49aa-b00b-aaa43bb63282",
        "products": [
            {
                "id": "SIHIL",
                "quantity": 1

            }
        ]
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/order/remove_products'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 201
    assert response.json['products'][0]['unit_price'] == 214500
    assert response.json['products'][0]['quantity'] == 10
    assert response.json['products'][0]['amount'] == 214500*10


def test_remove_items_from_non_existing_order(test_client):
    payload = {
        "order_id": "534dc18b-7525-49aa-b00b-aaa43bb63282",
        "products": [
            {
                "id": "SIHIL",
                "quantity": 1

            }
        ]
    }
    headers = {'Authorization': os.getenv('APP_TOKEN')}
    url = '/order/remove_products'
    response = test_client.post(url, headers=headers, json=payload)
    assert response.status_code == 404
    assert b'not found' in response.data
