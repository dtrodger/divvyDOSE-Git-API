"""
Pytest test fixtures
"""

import pytest
from flask.testing import FlaskClient

from api.app import app as flask_app


@pytest.fixture
def client() -> FlaskClient:
    """
    Flask test REST client
    """

    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client
