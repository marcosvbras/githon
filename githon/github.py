"""Module that contains all GitHub data scraping logic."""
import requests
from utils import BaseRequest
from repository import Repository
from exceptions import InvalidTokenError, UserIdNotFoundError, ApiError

__version__ = '0.9.0'


class Github(BaseRequest):
    """Class that controls all Github API v3 requests."""

    def __init__(self, access_token=None):
        """Constructor.

        Args:
            access_token: The default GitHub access_token.

        If you don't provide an access_token, your number of requests will be limited to 60 requests per hour, acording with GitHub REST API v3.
        See more in https://developer.github.com/v3/#rate-limiting
        """
        self.access_token = access_token

    def get_user_by_id(self, user_id, user_token=None, last_modified_date=None):
        """Get user by User ID.

        Args:
            user_id: The Github profile ID.
            user_token: GitHub OAuth2 access token.
            last_modified_date: Last modified Datetime.

        last_modified_date arg reduces request spends.
        See more in https://developer.github.com/v3/#conditional-requests

        Returns:
            dict: The Github profile data in json format.

        """
        url = "{0}/user/{1}{2}"
        headers = None

        if last_modified_date:
            headers = {
                'If-Modified-Since': self.convert_to_rfc1123(last_modified_date)
            }

        response = requests.get(
            url.format(
                self.ROOT_API_URL, user_id, self.get_token(user_token)
            ), headers=headers
        )

        if response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': user_token})
        elif response.status_code == requests.codes.not_found:
            raise UserIdNotFoundError({'user_id': user_id})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def get_user_emails(self, user_token, last_modified_date=None):
        """Retrieve a list of emails from a given user_token.

        Arguments:
            user_token: OAuth2 access token authorized by account owner.

        Returns:
            dict: The profile emails data in json format.
        """
        url = "{0}/user/emails?access_token={1}"
        headers = None

        if last_modified_date:
            headers = {
                'If-Modified-Since': self.convert_to_rfc1123(last_modified_date)
            }

        response = requests.get(
            url.format(self.ROOT_API_URL, user_token), headers=headers)

        if response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': user_token})
    elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def retrieve_private_github_email(self, user_id, access_token=None, last_modified_date=None):
        """Retrieve private email based in user commits.

        Args:
            user_id: The Github profile ID.
            access_token: GitHub OAuth2 access token.

        Returns:
            str: The private email or a no-reply Github email.

        """
        email = None
        keep_searching = True
        repository = Repository(access_token)

        repository_data = [
            i for i in repository.get_repositories_by_user_id(
                user_id, access_token) if not i['fork']
        ]

        if repository_data:
            for repository in repository_data:
                if not repository.fork:
                    commits_data = repository.get_commits_by_id(
                        repository.id, access_token)

                    for commit in commits_data:
                        if 'commit' in commit and commit['author'] and commit['author'].get('login', None) == username:
                            email = commit['commit']['author'].get(
                                'email', None)
                            keep_searching = False
                            break

                    if not keep_searching:
                        break

        return email
