"""
Bitbucket REST client

# TODO Switch to asyncio for multitasking with non blocking IO on HTTP requests
"""

import logging
import requests
from requests.auth import HTTPBasicAuth
import json

from flask import current_app


log = logging.getLogger(__name__)


BITBUCKET_API = "https://api.bitbucket.org/2.0"
bitbucket_basic_auth = None


def get_bitbucket_basic_auth(reset: bool = False) -> HTTPBasicAuth:
    """
    Gets a HTTPBasicAuth instance with BitBucket username and password
    """

    global bitbucket_basic_auth
    if not bitbucket_basic_auth or reset:
        bitbucket_basic_auth = HTTPBasicAuth(
            current_app.config["BITBUCKET_USERNAME"],
            current_app.config["BITBUCKET_PASSWORD"],
        )

    return bitbucket_basic_auth


def bitbucket_http_get(url: str, params: dict = None) -> dict:
    """
    Bitbucket HTTP GET
    """

    response_body = None
    try:
        response = requests.get(url, params=params, auth=get_bitbucket_basic_auth())
        assert response.status_code == 200
        response_body = json.loads(response.content)
    except Exception as e:
        log.info(f"{e}")

    return response_body


def bitbucket_http_get_pages(url: str, page: int = 1) -> list:
    """
    Bitbucket HTTP GET all paginated results
    """

    params = {"page": page, "pagelen": 100}
    pages = []
    response = bitbucket_http_get(url, params)
    if response:
        pages = pages + response["values"]
        if response.get("next"):
            page += 1
            pages = pages + bitbucket_http_get_pages(url, page)

    return pages


def bitbucket_team_profile(team: str) -> dict:
    """
    Builds a Bitbucket team's profile
    """

    team_public_repository_count = 0
    team_forked_repository_count = 0
    team_watchers_count = 0
    team_languages = set()
    for repository in bitbucket_http_get_pages(f"{BITBUCKET_API}/repositories/{team}"):
        team_public_repository_count += 1
        team_forked_repository_count += len(
            bitbucket_http_get_pages(repository["links"]["forks"]["href"])
        )
        team_watchers_count = len(
            bitbucket_http_get_pages(repository["links"]["watchers"]["href"])
        )
        team_languages.add(repository["language"])

    # TODO unable to find topics on BitBuckets API docs
    team_profile = {
        "public_repository_count": team_public_repository_count,
        "forked_repository_count": team_forked_repository_count,
        "watchers_count": team_watchers_count,
        "languages": {"distinct": list(team_languages), "count": len(team_languages)},
    }

    return team_profile
