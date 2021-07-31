import pytest

from app import make_app
from app.api.models import ClientModel, ProductModel, OrderModel


@pytest.fixture(scope='module')
def test_client():
    flask_app = make_app(testing=True)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
