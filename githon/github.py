# coding: utf-8
"""Module that contains all GitHub data scraping logic."""
import requests
from .utils import BaseRequest
from .exceptions import (InvalidTokenError, UserNotFoundError, ApiError,
                         InvalidQueryError, ApiRateLimitError)


class GithubApi(BaseRequest):
    """Class that controls all Github API v3 requests."""

    def __init__(self, default_access_token=None):
        """Constructor.

        Args:
            access_token: The default GitHub access_token.

        If you don't provide an access_token, your number of requests will be limited to 60 requests per hour, acording with GitHub REST API v3.
        See more in https://developer.github.com/v3/#rate-limiting
        """
        self.default_access_token = default_access_token

    def user_by_id(self, user_id, access_token=None, last_modified_date=None):
        """Get user by User ID.

        Args:
            user_id: The Github profile ID.
            access_token: GitHub OAuth2 access token.
            last_modified_date: Last modified Datetime.

        last_modified_date arg reduces request spends.
        See more in https://developer.github.com/v3/#conditional-requests.

        Returns:
            dict: A dictionary with Github profile data.

        """
        return self._complete_user_request(
            "user", user_id, access_token, last_modified_date)

    def user_by_username(self, username, access_token=None, last_modified_date=None):
        """Get user by username.

        Args:
            username: The Github profile username.
            access_token: GitHub OAuth2 access token.
            last_modified_date: Last modified Datetime.

        last_modified_date arg reduces request spends.
        See more in https://developer.github.com/v3/#conditional-requests.

        Returns:
            dict: A dictionary with Github profile data.

        """
        return self._complete_user_request(
            "users", username, access_token, last_modified_date)

    def user_emails(self, access_token):
        """Retrieve a list of emails from a given access_token.

        Arguments:
            access_token: OAuth2 access token authorized by account owner.

        Returns:
            dict: The profile emails data.

        """
        url = "{0}/user/emails?access_token={1}"
        response = requests.get(url.format(self.ROOT_API_URL, access_token))
        remaining = int(response.headers['X-RateLimit-Remaining'])

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError(
                {'X-RateLimit-Remaining': remaining,
                 'X-RateLimit-Limit': response.headers['X-RateLimit-Limit']})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def followers_by_id(self, user_id, access_token=None):
        """Return followers from a given User ID.

        Args:
            user_id: Github User ID.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's followers data.

        """
        return self._complete_resource_request(
            "user", user_id, "followers", access_token)

    def followers_by_username(self, username, access_token=None):
        """Return followers from a given username.

        Args:
            username: Github username.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's followers data.

        """
        return self._complete_resource_request(
            "users", username, "followers", access_token)

    def following_by_id(self, user_id, access_token=None):
        """Return following list from a given User ID.

        Args:
            user_id: Github User ID.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's following data.

        """
        return self._complete_resource_request(
            "user", user_id, "following", access_token)

    def following_by_username(self, username, access_token=None):
        """Return following list from a given username.

        Args:
            user_id: Github username.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's following data.

        """
        return self._complete_resource_request(
            "users", username, "following", access_token)

    def gists_by_id(self, user_id, access_token=None):
        """Return gists from a given User ID.

        Args:
            user_id: Github User ID.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's gist data.

        """
        return self._complete_resource_request(
            "user", user_id, "gists", access_token)

    def gists_by_username(self, username, access_token=None):
        """Return gists from a given username.

        Args:
            username: Github username.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's gist data.

        """
        return self._complete_resource_request(
            "users", username, "gists", access_token)

    def repositories_by_id(self, user_id, access_token=None):
        """Return repositories from a given User ID.

        Args:
            user_id: Github User ID.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's repositories data.

        """
        return self._complete_resource_request(
            "user", user_id, "repos", access_token)

    def repositories_by_username(self, username, access_token=None):
        """Return repositories from a given username.

        Args:
            username: Github username.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with summary user's repositories data.

        """
        return self._complete_resource_request(
            "users", username, "repos", access_token)

    def _complete_user_request(self, kind, user, access_token, last_modified_date):
        """Complements an user data request from a given User.

        Args:
            kind: 'users' if username passed or 'user' if user id passed.
            user: Github User ID or Username
            access_token: GitHub OAuth2 access token.
            last_modified_date: Last modified Datetime.

        last_modified_date arg reduces request spends.
        See more in https://developer.github.com/v3/#conditional-requests.

        Returns:
            dict: A dictionary with Github profile data.

        """
        url = "{0}/{1}/{2}{3}"
        headers = None
        data = {}
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "?access_token={}".format(access_token)

        if last_modified_date:
            headers = self.get_last_modified_header(last_modified_date)

        response = requests.get(
            url.format(self.ROOT_API_URL, kind, user, token_arg),
            headers=headers)

        self._check_status_code(response, user, access_token)

        if response.text != '':
            data = response.json()

        return data

    def _complete_resource_request(self, kind, user, complement, access_token):
        """Complements an user data request from a given User.

        Args:
            kind: 'users' if username passed or 'user' if user id passed.
            user: Github User ID or Username
            complement: A resource to be requested.
            access_token: GitHub OAuth2 access token.

        Returns:
            dict: A dictionary with requested data.

        """
        url = "{0}/{1}/{2}/{3}{4}"
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "?access_token={}".format(access_token)

        response = requests.get(url.format(
            self.ROOT_API_URL, kind, user, complement, token_arg))

        self._check_status_code(response, user, access_token)

        return response.json()

    def _check_status_code(self, response, user, access_token):
        """Check status codes and raise Exceptions if necessary.

        Args:
            response: HTTP Response object from requests library.
            user: Github UID or Username.
            access_token: GitHub OAuth2 access token.
        """
        remaining = int(response.headers['X-RateLimit-Remaining'])

        if response.status_code == requests.codes.not_found:
            raise UserNotFoundError({'user': user})
        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError(
                {'X-RateLimit-Remaining': remaining,
                 'X-RateLimit-Limit': response.headers['X-RateLimit-Limit']})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

    def search_users(self, query, page=1, per_page=100, access_token=None):
        """Retrieve users with a given query.

        Args:
            query: A Github query string.
            page: Controls the pagination.
            per_page: Controls the number os results per page.
            access_token: GitHub OAuth2 access token.
        Returns:
            dict: A list of Github users that matches with query.

        """
        # repos:>=1
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "&access_token={}".format(access_token)

        url = "{0}/search/users?q={1}&page={2}&per_page={3}&type=Users{4}"

        response = requests.get(
            url.format(self.ROOT_API_URL, self.encode_parameters(query), page,
                       per_page, token_arg))

        remaining = int(response.headers['X-RateLimit-Remaining'])

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError(
                {'X-RateLimit-Remaining': remaining,
                 'X-RateLimit-Limit': response.headers['X-RateLimit-Limit']})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code == requests.codes.not_found:
            raise InvalidQueryError()
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()
