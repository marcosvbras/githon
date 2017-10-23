# githon

[![Current version at PyPI](https://img.shields.io/pypi/v/githon.svg)](https://pypi.python.org/pypi/githon)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/githon.svg)
![Software status](https://img.shields.io/pypi/status/githon.svg)
[![PyPI](https://img.shields.io/pypi/l/githon.svg)]()
[![GitHub issues](https://img.shields.io/github/issues/marcosvbras/githon.svg)]()
[![GitHub forks](https://img.shields.io/github/forks/marcosvbras/githon.svg?style=social&label=Fork)]()
[![GitHub stars](https://img.shields.io/github/stars/marcosvbras/githon.svg?style=social&label=Stars)]()
[![Donate](https://img.shields.io/gratipay/marcosvbras.svg?style=social&label=Donate)](https://www.gratipay.com/marcosvbras)

**Githon** is a python library that provides a GitHub REST API v3 Data Scraping.

With this library you can:
- Request user data through username or user ID
- Control request errors easily
- Use Application tokens or Personal User tokens to request data
- Reduce spending on your requisition limit

## Installation
Run the command:

```
pip install githon
```

## How to use
Import the **GithubApi** class and create an object. Optionally pass an access token to constructor.

```
>>> from githon import GithubApi
>>> gh = GithubApi('YOUR_ACCESS_TOKEN')
```

> **NOTE**: With access_token, your rate limit will be 5000 requests per hour. If you don't provide an access_token, your number of requests will be limited to 60 requests per hour, according with GitHub REST API v3 docs.
See more in https://developer.github.com/v3/#rate-limitingUse.

Sample code:

```
>>> gh.user_by_username('marcosvbras')
{ 'blog': 'https://about.me/marcosvbras', 'followers': 7, 'following': 28, ...}
```

## Methods
- ```user_by_username```: Request user based in Github login.
- ```user_by_id```: Request user based in Github User ID.
- ```user_emails```: Retrieve a list of emails from a given access_token. Requires the user access token.
- ```followers_by_id```: Request the user followers based in Github login.
- ```followers_by_username```: Request the user followers based in Github ID.
- ```following_by_id```: Request the user following based in Github ID.
- ```following_by_username```: Request the user following based in Github login.
- ```gists_by_id```: Request the user gists based in Github ID.
- ```gists_by_username```: Request the user gists based in Github login.
- ```repositories_by_id```: Request the user repositories based in Github ID.
- ```repositories_by_username```: Request the user repositories based in Github login.
- ```search_users```: Search users with a Github query.
- ```get_request_limit```: Request the API Rate Limit to your token.
