import requests

__version__ = '0.9'

class Githon:
    """Class that controls all Github API v3 requests."""

    def get_user_by_id(self, uid, user_token=None):
        """Get user by User ID.

        This method uses /user/{id} endpoint. The default /users/{username} used for original library not accept ID.
        """
        if not uid:
            return None

        url = "https://api.github.com/user/{0}?access_token={1}"
        response = requests.get(url.format(uid, self.get_token(user_token)))

        if response.status_code == 404:
            raise Exception("Error 404: User Id '{}' not found in GitHub REST API".format(uid))

        return response.json()

    def get_repository_contribution(self, repository_id, user_token):
        """Return user repositories by repository_id."""
        if not repository_id:
            return None

        contributions = None

        url = "https://api.github.com/repositories/{0}?access_token={1}"
        response = requests.get(url.format(repository_id, self.get_token()))
        data = response.json()

        if 'contributors_url' in data:
            response = requests.get(data['contributors_url'])
            data = response.json()
            if 'contributions' in data:
                contributions = data['contributions']

        return contributions

    def get_user_email(self, user_token):
        """Return logged in user email."""
        # TO DO: Exception if not has token
        # Wrong access_token returns 401 Unauthorized
        # Right acess_token returns 304 Not Modified
        if not user_token:
            return None

        url = "https://api.github.com/user/emails?access_token={}"
        response = requests.get(url.format(user_token))

        return response.json()

    def get_repository_commits(self, username, repository_name, user_token):
        """Return repository commits from a given username."""
        url = "https://api.github.com/repos/{0}/{1}/commits?access_token={2}"
        response = requests.get(
            url.format(username, repository_name, self.get_token(user_token)))

        return response.json()

    def get_token(self, user_token):
        """Return the access token argument if exists or None."""
        if user_token:
            return "?access_token={}".format(user_token)
        elif self.access_token:
            return "?access_token={}".format(self.access_token)
        else:
            return None


    def retrieve_private_github_email(self, username, access_token=None):
    """Retrieve private email based in user commits."""
    email = None
    keep_searching = True

    try:
        # repository_data = [i for i in github_api.users_repos(github.login, 'owner', user_token) if not i['fork']]

        if repository_data:
            for repository in repository_data:
                if not repository.fork:
                    commits_data = self.get_repository_commits(
                        username, repository.name, access_token)

                    for commit in commits_data:
                        if 'commit' in commit and commit['author'] and commit['author'].get('login', None) == username:
                            email = commit['commit']['author'].get('email', None)
                            keep_searching = False
                            break

                    if not keep_searching:
                        break
    except Exception as ex:
        pass

    def verify_request_limit(self, response):
        # X-RateLimit-Limit      X-RateLimit-Reset
        return response.headers['X-RateLimit-Remaining'] > 0
