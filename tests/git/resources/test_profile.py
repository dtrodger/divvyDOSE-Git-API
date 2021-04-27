"""
GitProfileResource test module
"""

from flask.testing import FlaskClient


def test_get_git_profile(client: FlaskClient) -> None:
    """
    GitProfileResource GET unit test
    """

    assert True