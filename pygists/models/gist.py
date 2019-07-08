"""
Github gist model
"""
from collections import namedtuple
import datetime as dt

GistFile = namedtuple(
    'GistFiles', ('filename', 'type', 'language', 'raw_url', 'size', 'truncated', 'content'),
    defaults=(None, None)
)
GistOwner = namedtuple(
    'GistOwner', (
        'login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url', 'followers_url',
        'following_url', 'gists_url', 'starred_url', 'subscriptions_url', 'organizations_url',
        'repos_url', 'events_url', 'received_events_url', 'type', 'site_admin'
    )
)


class Gist:

    __slots__ = [
        'url', 'forks_url', 'commits_url', 'id', 'node_id', 'git_pull_url', 'git_push_url',
        'html_url', 'files', 'public', 'created_at', 'updated_at', 'description',
        'comments', 'user', 'comments_url', 'owner', 'truncated', 'script_url'
    ]
    _transformations = {
        'created_at': lambda _: dt.datetime.strptime(_, '%Y-%m-%dT%H:%M:%SZ'),
        'updated_at': lambda _: dt.datetime.strptime(_, '%Y-%m-%dT%H:%M:%SZ'),
        'files': lambda files: [GistFile(**_) for _ in files],
        'owner': lambda _: GistOwner(**_),
    }

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, self._transformations.get(key, lambda _: _)(value))

    @classmethod
    def from_response(cls, resp):
        """To be called with json response from GitHub API. Adds script_url and flattens files."""
        resp['script_url'] = 'https://gist.github.com/{user}/{gist_id}.js'.format(
            user=resp['owner']['login'], gist_id=resp['id']
        )

        files = []
        for file in resp['files'].values():
            files.append({k: v for k, v in file.items()})

        resp['files'] = files

        resp.pop('history', None)  # TODO: handle forks, history
        resp.pop('forks', None)

        return cls(**resp)

    def describe(self):
        print(
            f"{self.owner.login}'s GitHub Gist: {self.files[0].filename}\n"
            f"'{self.description}'\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Embed: {self.script_url}\n"
            "File | Size (chars)"
        )
        for file in self.files:
            print(f'{file.filename}', '|', f'{file.size}')
        print('\n')
