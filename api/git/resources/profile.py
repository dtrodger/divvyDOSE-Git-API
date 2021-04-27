"""
Git app Profile API resource
"""
import logging

from flask_restful import Resource

from api.utils import authenticate_token
from api.git.github_ import github_organization_profile
from api.git.bitbucket import bitbucket_team_profile
from api.utils import APIException


log = logging.getLogger(__name__)


class GitProfileResource(Resource):
    """
    Git app Profile API resource
    """

    method_decorators = [authenticate_token]

    def get(self, profile: str = None) -> dict:
        """
        HTTP GET /git/profile/[profile]/ request handler
        """

        # TODO - Integrate caching for a faster response
        try:
            response_body = {
                "profile_for": profile,
                "github_profile": github_organization_profile(profile),
                "bitbucket_profile": bitbucket_team_profile(profile),
            }
        except Exception as e:
            # TODO - Catch lower level exceptions within the github_ and bitbucket modules for more useful API
            # error messages
            log.error(f"Git app Profile resource GET failed with {e}")
            raise APIException(f"Failed to build Git profile for {profile}")

        return response_body
