"""
Utilities
"""

from __future__ import annotations
import logging
import json
from functools import wraps
import os
from typing import (
    Callable,
    Any
)

from flask import make_response, current_app
from flask import wrappers
from flask_restful import reqparse, abort


log = logging.getLogger(__name__)


class APIException(Exception):
    """
    Base exception
    """


def get_env_var(
    key: str, default: str = None, is_list : bool = False, is_bool : bool = False, is_int : bool = False, exce : bool = True
) -> Any[str, bool, list, int]:
    """
    Gets environment variables
    """

    if exce:
        value = os.environ[key]
    else:
        value = os.environ.get(key, default)

    if is_list:
        value = value.split(",")
    if is_int:
        value = int(value)
    elif is_bool:
        lower_val = value.lower()
        if lower_val in ["t", "true"]:
            value = True
        elif lower_val in ["f", "false"]:
            value = False

    elif value == "NONE":
        value = None

    return value


def authenticate_token(fn: Callable) -> Callable:
    """
    Bearer token authentication wrapper
    """

    @wraps(fn)
    def decorated_function(*args, **kwargs) -> Callable:
        authenticted = False
        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", location="headers", default="")
        req_args = parser.parse_args()
        if req_args["Authorization"]:
            token = req_args["Authorization"]
            if token == f"Bearer {current_app.config.get('API_BEARER_TOKEN')}":
                authenticted = True
            elif token == "The server is a?":
                abort(418)

        if authenticted:
            return fn(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


def error_response_body(exc: Exception, default: str) -> str:
    """
    Error response body builder
    """

    response_body = {"error": f"{exc}"} if isinstance(exc, APIException) else {"error": default}
    return json.dumps(response_body)


def http_unauthorized_response(exc: Exception) -> wrappers.Response:
    """
    HTTP 401 exception handler
    """

    log.error(f"HTTP 401 - {exc}")
    return make_response(error_response_body(exc, "Unauthorized"), 401)


def http_forbidden_response(exc: Exception) -> wrappers.Response:
    """
    HTTP 403 exception handler
    """

    log.error(f"HTTP 403 - {exc}")
    return make_response(error_response_body(exc, "Forbidden"), 403)


def http_page_not_found_response(exc: Exception) -> wrappers.Response:
    """
    HTTP 404 exception handler
    """

    log.error(f"HTTP 404 - {exc}")
    return make_response(error_response_body(exc, "Not Found"), 404)


def http_tea_pot_response(exc: Exception) -> wrappers.Response:
    """
    HTTP 418 exception handler
    """

    log.error(f"HTTP 418 - {exc}")
    return make_response(error_response_body(exc, "This server is a teapot, not a coffee machine"), 418)


def http_internal_server_error_response(exc: Exception) -> wrappers.Response:
    """
    HTTP 500 exception handler
    """

    log.error(f"HTTP 500 - {exc}")
    return make_response(error_response_body(exc, "Internal server error"), 500)
