# coding: utf-8
"""Module that contains all user repository Data Scraping logic."""

import requests
from .utils import BaseRequest
from .exceptions import (InvalidTokenError, RepositoryNameNotFoundError,
                         ApiError, RepositoryIdNotFoundError, ApiRateLimitError)


class RepositoryApi(BaseRequest):
    """Class that has Repository Data Scraping actions."""

    def __init__(self, default_access_token=None):
        """Constructor.

        Args:
            default_access_token: The default GitHub access_token

        If you don't provide an access_token, your number of requests will be limited to 60 requests per hour, acording with GitHub REST API v3.
        """
        self.default_access_token = default_access_token

    def repository_by_id(self, repository_id, access_token=None):
        """Return a repository with given repository ID."""
        url = "{0}/repositories/{1}{2}"
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "?access_token={}".format(access_token)

        response = requests.get(
            url.format(self.ROOT_API_URL, repository_id, token_arg))

        self._check_common_status_code(response, access_token)

        if response.status_code == requests.codes.not_found:
            raise RepositoryIdNotFoundError({'repository_id': repository_id})

        return response.json()

    def repository_by_name(self, username, repository_name, access_token=None):
        """Return a repository with given repository_name and username."""
        url = "{0}/repos/{1}/{2}{3}"
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "?access_token={}".format(access_token)

        response = requests.get(
            url.format(
                self.ROOT_API_URL, username, repository_name, token_arg)
        )

        self._check_common_status_code(response, access_token)

        if response.status_code == requests.codes.not_found:
            raise RepositoryNameNotFoundError(
                {'repository_name': repository_name, 'username': username})

        return response.json()

    def get_all_data(self, repository_id=None, repository_name=None, access_token=None):
        """Request all repository data from a given repository ID or name."""
        data = {}

        if repository_id:
            root_data = self.repository_by_id(repository_id, access_token)
            data['id'] = root_data['id']
            data['name'] = root_data['name']
            data['private'] = root_data['private']
            data['description'] = root_data['description']
            data['fork'] = root_data['fork']
            data['id'] = root_data['id']
            data['created_at'] = root_data['created_at']
            data['updated_at'] = root_data['updated_at']
            data['pushed_at'] = root_data['pushed_at']
            data['homepage'] = root_data['homepage']
            data['size'] = root_data['size']
            data['stargazers_count'] = root_data['stargazers_count']
            data['watchers_count'] = root_data['watchers_count']
            data['language'] = root_data['language']
            data['has_issues'] = root_data['has_issues']
            data['has_projects'] = root_data['has_projects']
            data['has_downloads'] = root_data['has_downloads']
            data['has_wiki'] = root_data['has_wiki']
            data['has_pages'] = root_data['has_pages']
            data['forks_count'] = root_data['forks_count']
            data['mirror_url'] = root_data['mirror_url']
            data['archived'] = root_data['archived']
            data['open_issues_count'] = root_data['open_issues_count']
            data['forks'] = root_data['forks']
            data['open_issues'] = root_data['open_issues']
            data['watchers'] = root_data['watchers']
            data['default_branch'] = root_data['default_branch']
            data['network_count'] = root_data['network_count']
            data['subscribers_count'] = root_data['subscribers_count']

            data['branches'] = self.get_branches_by_id(
                repository_id, access_token)
            data['comments'] = self.get_comments_by_id(
                repository_id, access_token)
            data['commits'] = self.get_commits_by_id(
                repository_id, access_token)
            data['contents'] = self.get_contents_by_id(
                repository_id, access_token)
            data['contributors'] = self.get_contributors_by_id(
                repository_id, access_token)
            data['events'] = self.get_events_by_id(
                repository_id, access_token)
            data['issues'] = self.get_issues_by_id(
                repository_id, access_token)
            data['labels'] = self.get_labels_by_id(
                repository_id, access_token)
            data['languages'] = self.get_languages_by_id(
                repository_id, access_token)
            data['pulls'] = self.get_pulls_by_id(
                repository_id, access_token)
            data['subscribers'] = self.get_subscribers_by_id(
                repository_id, access_token)
            data['tags'] = self.get_tags_by_id(
                repository_id, access_token)

        return data

    def commits_by_name(self, username, repository_name, access_token):
        """Return repository commits from a given username.

        Arguments:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "commits", access_token)

    def contributors_by_name(self, username, repository_name, access_token):
        """Return repository contributors from a given username.

        Arguments:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "contributors", access_token)

    def issues_by_name(self, username, repository_name, access_token):
        """Return repository issues from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "issues", access_token)

    def events_by_name(self, username, repository_name, access_token):
        """Return repository events from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "events", access_token)

    def branches_by_name(self, username, repository_name, access_token):
        """Return repository branches from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "branches", access_token)

    def tags_by_name(self, username, repository_name, access_token):
        """Return repository tags from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "tags", access_token)

    def languages_by_name(self, username, repository_name, access_token):
        """Return repository languages from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "languages", access_token)

    def subscribers_by_name(self, username, repository_name, access_token):
        """Return repository subscribers from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "subscribers", access_token)

    def comments_by_name(self, username, repository_name, access_token):
        """Return repository comments from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "comments", access_token)

    def contents_by_name(self, username, repository_name, access_token):
        """Return repository contents from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "contents", access_token)

    def pulls_by_name(self, username, repository_name, access_token):
        """Return repository pulls from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "pulls", access_token)

    def labels_by_name(self, username, repository_name, access_token):
        """Return repository labels from a given username.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_name(
            username, repository_name, "labels", access_token)

    def commits_by_id(self, repository_id, access_token=None):
        """Return repository commits from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "commits", access_token)

    def contributors_by_id(self, repository_id, access_token=None):
        """Return repository contributors from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "contributors", access_token)

    def issues_by_id(self, repository_id, access_token=None):
        """Return repository issues from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "issues", access_token)

    def events_by_id(self, repository_id, access_token=None):
        """Return repository events from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "events", access_token)

    def branches_by_id(self, repository_id, access_token=None):
        """Return repository branches from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "branches", access_token)

    def tags_by_id(self, repository_id, access_token=None):
        """Return repository tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(repository_id, "tags", access_token)

    def languages_by_id(self, repository_id, access_token=None):
        """Return languages tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "languages", access_token)

    def subscribers_by_id(self, repository_id, access_token=None):
        """Return subscribers tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "subscribers", access_token)

    def comments_by_id(self, repository_id, access_token=None):
        """Return comments tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "comments", access_token)

    def contents_by_id(self, repository_id, access_token=None):
        """Return contents tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "contents", access_token)

    def pulls_by_id(self, repository_id, access_token=None):
        """Return pulls tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "pulls", access_token)

    def labels_by_id(self, repository_id, access_token=None):
        """Return labels tags from a given username and repository ID.

        Args:
            repository_id: An existent user's repository ID.
            access_token: GitHub OAuth2 access token.
        """
        return self._complete_request_by_id(
            repository_id, "labels", access_token)

    def _complete_request_by_name(self, username, repository_name, complement, access_token):
        """Complements a repository data request by name.

        Args:
            username: Github username.
            repository_name: An existent user's repository name.
            access_token: GitHub OAuth2 access token.
        """
        url = "{0}/repos/{1}/{2}/{3}{4}"
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "?access_token={}".format(access_token)

        response = requests.get(
            url.format(
                self.ROOT_API_URL, username, repository_name, complement,
                token_arg
            )
        )

        self._check_common_status_code(response, access_token)

        if response.status_code == requests.codes.not_found:
            raise RepositoryNameNotFoundError(
                {'repository_name': repository_name, 'username': username})

        return response.json()

    def _complete_request_by_id(self, repository_id, complement, access_token):
        """Complements a repository data request by ID.

        Args:
            repository_id: An existent user's repository ID.
            complement: A resource to be requested.
            access_token: GitHub OAuth2 access token.
        """
        url = "{0}/repositories/{1}/{2}{3}"
        access_token = self.get_token(access_token)
        token_arg = ''

        if access_token != '':
            token_arg = "?access_token={}".format(access_token)

        response = requests.get(
            url.format(self.ROOT_API_URL, repository_id, complement, token_arg))

        self._check_common_status_code(response, access_token)

        if response.status_code == requests.codes.not_found:
            raise RepositoryIdNotFoundError({'repository_id': repository_id})

        return response.json()

    def _check_common_status_code(self, response, access_token):
        remaining = int(response.headers['X-RateLimit-Remaining'])

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError(
                {'X-RateLimit-Remaining': remaining,
                 'X-RateLimit-Limit': response.headers['X-RateLimit-Limit']})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()
