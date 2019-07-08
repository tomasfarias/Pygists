import datetime as dt
from typing import List, Sequence, Union
from urllib.parse import urljoin

import requests

from pygists.models.gist import Gist


BASE_ENDPOINT = 'https://api.github.com/'


class Pygists:

    def __init__(self, username: str, token_path: str) -> None:
        self.username = username
        self.token_path = token_path
        self.session = self.start_session()

    def start_session(self) -> requests.Session:
        """Read OAuth token and set session authorization parameters"""
        with open(self.token_path, 'r') as f:
            token = f.read()

        session = requests.Session()
        session.auth = (self.username, token)
        return session

    def create_gist(
            self, names: Sequence[str], contents: Sequence[str], description: str, public: bool
    ) -> Gist:
        """Create gist with the GitHub API"""

        if len(names) != len(contents):
            raise ValueError('Length of names and contents differs.')

        endpoint = urljoin(BASE_ENDPOINT, 'gists')
        files = {name: {'content': content} for name, content in zip(names, contents)}
        params = {
            'files': files,
            'description': description,
            'public': public
        }

        r = self.session.post(endpoint, json=params)
        r.raise_for_status()

        return Gist.from_response(r.json())

    def get_gists(self, since: dt.datetime = None) -> List:
        """Get all user's public gists"""
        endpoint = urljoin(BASE_ENDPOINT, f'users/{self.username}/gists')

        r = self.session.get(
            endpoint,
            params={'since': since.strftime('%Y-%m-%dT%H:%M:%SZ')} if since is not None else None
        )
        return [Gist.from_response(gist) for gist in r.json()]

    def edit_gist(
        self, gist_id: str, names: Sequence[str], contents: Sequence[str], description: str
    ) -> Gist:
        """Edit a single gist"""
        endpoint = urljoin(BASE_ENDPOINT, f'gists/{gist_id}')
        files = {name: {'content': content} for name, content in zip(names, contents)}
        params = {
            'files': files,
            'description': description
        }

        r = self.session.patch(endpoint, json=params)
        r.raise_for_status()

        return Gist.from_response(r.json())

    def get_or_create_gist(
            self, names: Sequence[str], contents: Sequence[str], description: str, public: bool
    ) -> Union[Gist, List[Gist]]:
        """
        Get all gists, check if a gist exists with given file names and create it if it doesn't
        """

        if len(names) != len(contents):
            raise ValueError('Length of names and contents differs.')

        current_gists = self.get_gists()

        for gist in current_gists:
            if sorted(gist['files'].keys()) == sorted(names):
                return gist

        return self.create_gist(names, contents, description, public)
