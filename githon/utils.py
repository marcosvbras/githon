# coding: utf-8
"""Module with connection utilities."""

import requests
import urllib.parse
from dateutil.parser import parse
from .exceptions import InvalidDateTimeFormat


class BaseRequest:
    """Contains common actions to library."""

    ROOT_API_URL = 'https://api.github.com'

    def get_request_limit(self, access_token):
        """Request Github remaining requests without spend the amount remaining.

        Args:
            access_token: The target access_token.
        Returns:
            int: The amount of remaining requests for a given access_token.

        """
        url = "{0}/rate_limit?access_token={1}"
        response = requests.get(url.format(self.ROOT_API_URL, access_token))
        data = response.json()
        return data['resources']['core'].get("remaining")

    def get_last_modified_header(self, datetime):
        """Return a header with If-Modified-Since attribute.

        Args:
            datetime: The string datetime to be converted.

        Returns:
            dict: The personalized header.

        """
        new_date_format = self._convert_to_rfc1123(datetime)

        return {'If-Modified-Since': new_date_format}

    def _convert_to_rfc1123(self, datetime):
        """Convert an datetime string to RFC1123 format.

        Example
            Input: 2017-10-13T03:03:57Z
            Output: Fri, 13 Oct 2017 03:03:57 GMT

        Args:
            datetime: The string datetime to be converted.
        Returns:
            str: Datetime in RFC1123 format.

        """
        try:
            new_date_format = parse('2017-10-13T03:03:57Z').strftime(
                '%a, %d %b %Y %H:%M:%S GMT')
        except Exception as ex:
            raise InvalidDateTimeFormat({'datetime': datetime})

        return new_date_format

    def get_token(self, access_token):
        """Choose an access_token to be used for each request.

        Args:
            access_token: The priority access_token to be used.
        Returns:
            str: The access_token if exists or None.

        """
        if access_token:
            return access_token
        elif self.default_access_token:
            return self.default_access_token
        else:
            return ''

    def encode_parameters(self, text):
        """Encode special characters to URL pattern.

        Args:
            text: The text to be encoded.

        Returns:
            str: The encoded text.

        """
        return urllib.parse.quote_plus(text)
