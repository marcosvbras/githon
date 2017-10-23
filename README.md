# githon

[![Current version at PyPI](https://img.shields.io/pypi/v/githon.svg)](https://pypi.python.org/pypi/githon)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/githon.svg)
![Software status](https://img.shields.io/pypi/status/githon.svg)
[![PyPI](https://img.shields.io/pypi/l/githon.svg)]()
[![GitHub issues](https://img.shields.io/github/issues/marcosvbras/githon.svg)]()
[![GitHub forks](https://img.shields.io/github/forks/marcosvbras/githon.svg?style=social&label=Fork)]()
[![GitHub stars](https://img.shields.io/github/stars/marcosvbras/githon.svg?style=social&label=Stars)]()
[![Donate](https://img.shields.io/gratipay/marcosvbras.svg?style=social&label=Donate)](https://www.gratipay.com/marcosvbras)

**Githon** is a Python GitHub REST API v3 Data Scraping library that try request user data make simple.

With this library you can:
- Request user data through username or user ID
- Controls request errors easily
- Use Application tokens or Personal User tokens to request data
- Reduce request rate spends

## Installation
Run the command:

```
pip install githon
```

## How to use
Import the **GithubApi** class:

```
>>> from githon import GithubApi
```

Create an object and optionally pass an access token to constructor:

```
>>> gh = GithubApi('YOUR_ACCESS_TOKEN')
```

> NOTE: If you don't provide an access_token, your number of requests will be limited to 60 requests per hour, acording with GitHub REST API v3.
See more in https://developer.github.com/v3/#rate-limitingUse.

Sample code:

```
>>> gh.user_by_username('marcosvbras')
{ 'blog': 'https://about.me/marcosvbras', 'followers': 7, 'following': 28, ...}
```
