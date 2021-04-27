"""
Flask application entrypoint
"""

import os
from logging.config import dictConfig

from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from api.utils import (
    http_forbidden_response,
    http_unauthorized_response,
    http_internal_server_error_response,
    http_page_not_found_response,
    http_tea_pot_response,
    get_env_var,
)

from api.git.resources.profile import GitProfileResource


ENV_FILE_PATH = os.path.join(os.path.dirname(__file__), '../.env')


def create_app() -> Flask:
    """
    Sets up a Flask application
    """

    # Load the .env file into environment variables
    load_dotenv(ENV_FILE_PATH)
    # Configure logging
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "stdout": {"class": "logging.StreamHandler", "formatter": "standard"},
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": "logs/api.log",
                "mode": "a",
                "maxBytes": 1048576,
                "backupCount": 10,
            },
        },
        "loggers": {
            "": {
                "handlers": ["stdout", "file"],
                "level": get_env_var("DIVVYDOSE_LOG_LEVEL"),
            }
        },
    })
    # Instantiate a Flask application
    flask_app = Flask(get_env_var("DIVVYDOSE_API_NAME"), static_folder=None)
    # Set the Flask app's configuration from environment variables
    flask_app.config["API_BEARER_TOKEN"] = get_env_var("DIVVYDOSE_API_BEARER_TOKEN")
    flask_app.config["GITHUB_API_TOKEN"] = get_env_var("DIVYYDOSE_GITHUB_API_TOKEN")
    flask_app.config["BITBUCKET_USERNAME"] = get_env_var("DIVYYDOSE_BITBUCKET_USERNAME")
    flask_app.config["BITBUCKET_PASSWORD"] = get_env_var("DIVYYDOSE_BITBUCKET_PASSWORD")
    # Register HTTP error handlers
    flask_app.register_error_handler(401, http_unauthorized_response)
    flask_app.register_error_handler(403, http_forbidden_response)
    flask_app.register_error_handler(404, http_page_not_found_response)
    flask_app.register_error_handler(418, http_tea_pot_response)
    flask_app.register_error_handler(500, http_internal_server_error_response)
    flask_app.register_error_handler(Exception, http_internal_server_error_response)
    # Instantiate a Flask-RESTful instance
    rest_api = Api(flask_app)
    # Register a Flask-RESTful resource
    rest_api.add_resource(GitProfileResource, "/api/git/profile/<profile>/", endpoint="git-profile")

    return flask_app


app = create_app()
