"""
GitHub REST client

# TODO Switch to asyncio for multitasking with non blocking IO on HTTP requests
"""

from flask import current_app
from github import Github


github_client = None


def get_github_client(reset:bool = False) -> Github:
    """
    Sets up a GitHub client
    """

    global github_client
    if not github_client or reset:
        github_client = Github(current_app.config["GITHUB_API_TOKEN"])

    return github_client


def github_organization_profile(organization_name: str) -> dict:
    """
    Builds a GitHub organization's profile
    """

    github_client = get_github_client()
    organization = github_client.get_organization(organization_name)
    organization_public_repository_count = 0
    organization_forked_repository_count = 0
    organization_watchers_count = 0
    organization_languages = set()
    organization_topics = set()
    for repository in organization.get_repos():
        organization_public_repository_count += 1
        organization_forked_repository_count += repository.forks_count
        organization_watchers_count += repository.watchers_count
        repository_language = repository.language
        if repository_language:
            organization_languages.add(repository_language)

        repository_topics = repository.get_topics()
        if repository_topics:
            organization_topics.update(repository_topics)

    organization_profile = {
        "public_repository_count": organization_public_repository_count,
        "forked_repository_count": organization_forked_repository_count,
        "watchers_count": organization_watchers_count,
        "languages": {
            "distinct": list(organization_languages),
            "count": len(organization_languages),
        },
        "topics": {
            "distinct": list(organization_topics),
            "count": len(organization_topics),
        },
    }

    return organization_profile
