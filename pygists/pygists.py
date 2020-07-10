import datetime as dt
from typing import List, Sequence, Union, Optional, Dict
from urllib.parse import urljoin
from pathlib import Path
import os

import requests

from pygists.models.gist import Gist


BASE_ENDPOINT = 'https://api.github.com/'


class Pygists:
    def __init__(self, username: str, token: str) -> None:
        self.username = username
        self.token = token
        self._session = None

    @property
    def session(self):
        """Set session authorization parameters"""
        if self._session is None:
            self._session = requests.Session()
            self._session.auth = (self.username, self.token)
            self._session.headers.update({
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': self.username,
            })
        return self._session

    def create_gist_from_files(
        self, *args: Union[str, bytes, os.PathLike], description: str = '', public: bool = True
    ) -> Gist:
        names = []
        contents = []
        for file in args:
            p = Path(str(file))
            with open(p, 'r') as f:
                names.append(p.name)
                contents.append(f.read())

        return self.create_gist(names, contents, description, public)

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

    def edit_gist_from_files(
        self, to_add: Sequence[Union[str, bytes, os.PathLike]],
        to_delete: Sequence[Union[str, bytes, os.PathLike]],
        to_modify: Dict[str, Union[str, bytes, os.PathLike]],
        gist_id: str, description: Optional[str] = None,
    ) -> Gist:
        files: Dict[str, Optional[Union[Dict[str, str], str]]] = {}

        for file in to_add:
            p = Path(str(file))
            with open(p, 'r') as f:
                files[p.name] = {'content': f.read()}

        for name in to_delete:
            files[p.name] = None

        for old_name, new_file in to_modify.items():
            p = Path(str(file))
            with open(p, 'r') as f:
                files[old_name] = {'content': f.read(), 'filename': p.name}

        return self.edit_gist(
            gist_id=gist_id,
            files=files if files else None,
            new_description=description if description is not None else None
        )

    def edit_gist(
        self, gist_id: str, files: Optional[Dict[str, Optional[Union[Dict[str, str], str]]]] = None,
        new_description: Optional[str] = None
    ) -> Gist:
        """Edit a single gist"""
        endpoint = urljoin(BASE_ENDPOINT, f'gists/{gist_id}')
        if files is None and new_description is None:
            raise ValueError('No new description or files to edit gist')

        params = {}
        if files is not None:
            params['files'] = files  # type: ignore
        if new_description is not None:
            params['description'] = new_description  # type: ignore

        r = self.session.patch(endpoint, json=params)
        r.raise_for_status()

        return Gist.from_response(r.json())

    def list_user_gists(self, since: Optional[dt.datetime] = None) -> List[Gist]:
        """List all user's public gists"""
        endpoint = urljoin(BASE_ENDPOINT, f'users/{self.username}/gists')

        r = self.session.get(
            endpoint,
            params={'since': since.isoformat()} if since is not None else None
        )
        return [Gist.from_response(gist) for gist in r.json()]

    def get_gist(self, gist_id: str) -> Gist:
        """Get a user's gist"""
        endpoint = urljoin(BASE_ENDPOINT, f'/gists/{gist_id}')

        r = self.session.get(
            endpoint,
        )
        return Gist.from_response(r.json())

    def delete_gist(self, gist_id: str):
        """Delete a user's gist"""
        endpoint = urljoin(BASE_ENDPOINT, f'/gists/{gist_id}')

        r = self.session.delete(
            endpoint,
        )
        if r.status_code > 204:
            print(f'Delete operation failed: {r.json()}')
