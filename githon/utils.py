"""Module with connection utilities."""

import requests


class BaseRequest:
    """Contains common actions to library."""

    ROOT_API_URL = 'https://api.github.com'

    def get_request_limit(self, access_token):
        """Return the amount of remaining requests for a given access_token."""
        url = "{0}/rate_limit?access_token={1}"
        response = requests.get(
            url.format(self.ROOT_API_URL, self.access_token))
        data = response.json()
        return data['rate'].get("remaining")

    def get_token(self, user_token):
        """Return the access token argument if exists or None.

        Arguments:
            user_token -- The priority access_token
        """
        if user_token:
            return "?access_token={}".format(user_token)
        elif self.access_token:
            return "?access_token={}".format(self.access_token)
        else:
            return None
