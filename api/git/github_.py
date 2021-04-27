"""
GitHub REST client

# TODO Switch to asyncio for multitasking with non blocking IO on HTTP requests
"""

from flask import current_app
from github import (
    Github,
    Organization,
    Repository
)


github_client = None


def get_github_client(reset:bool = False) -> Github:
    """
    Sets up a GitHub client
    """

    global github_client
    if not github_client or reset:
        print(current_app.config["GITHUB_API_TOKEN"])
        github_client = Github(current_app.config["GITHUB_API_TOKEN"])

    return github_client


def github_organization(github_client: Github, organization: str) -> Organization:
    """
    Gets a GitHub organization
    """

    return github_client.get_organization(organization)


def github_repositories(organization: Organization) -> list:
    """
    Gets a GitHub organizations repositories
    """

    return organization.get_repos()


def github_repository_forks(repository: Repository) -> int:
    """
    Gets a count of GitHub repository forks
    """

    return repository.forks_count


def github_repository_language(repository: Repository) -> str:
    """
    Gets a repositories language
    """

    return repository.language


def github_repository_watchers(repository: Repository) -> list:
    """
    Gets a repositories watchers
    """

    return repository.watchers_count


def github_repository_topics(repository: Repository) -> list:
    """
    Gets a repositories topics
    """

    return repository.get_topics()


def github_organization_profile(organization_name: str) -> dict:
    """
    Builds a GitHub organization's profile
    """

    github_client = get_github_client()
    organization = github_organization(github_client, organization_name)
    organization_public_repository_count = 0
    organization_forked_repository_count = 0
    organization_watchers_count = 0
    organization_languages = set()
    organization_topics = set()
    for repository in github_repositories(organization):
        organization_public_repository_count += 1
        organization_forked_repository_count += github_repository_forks(repository)
        organization_watchers_count += github_repository_watchers(repository)
        repository_language = repository.language
        if repository_language:
            organization_languages.add(repository_language)

        repository_topics = github_repository_topics(repository)
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
