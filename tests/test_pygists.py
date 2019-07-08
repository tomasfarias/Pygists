import datetime as dt
import unittest.mock

import pytest

from pygists import Pygists
from pygists.cli import create_parser


@pytest.fixture
def gist(tmpdir):
    fh = tmpdir.join('token.txt')
    fh.write('testtoken')

    return Pygists('testuser', fh)


def test_pygist_init(gist):
    assert gist.session.auth == ('testuser', 'testtoken')


@unittest.mock.patch('requests.Session.post')
def test_create_single_gist_request(mock_post, gist):
    """Single name and content gist request respects docs format"""

    gist.create_gist(['test.py'], ['print("Hello World!")'], 'Testing', True)

    mock_post.assert_called_once_with(
        'https://api.github.com/gists',
        json={
            'files': {'test.py': {'content': 'print("Hello World!")'}},
            'description': 'Testing',
            'public': True
        }
    )


@unittest.mock.patch('requests.Session.post')
def test_create_multiple_gist_request(mock_post, gist):
    """Multiple names and contents gist request respects docs format"""

    gist.create_gist(
        ['test.py', 'test2.py'],
        ['print("Hello World!")', 'print("Bye World!")'],
        'Testing',
        True
    )

    mock_post.assert_called_once_with(
        'https://api.github.com/gists',
        json={
            'files': {
                'test.py': {'content': 'print("Hello World!")'},
                'test2.py': {'content': 'print("Bye World!")'}
            },
            'description': 'Testing',
            'public': True
        }
    )


@unittest.mock.patch('requests.Session.get')
def test_get_gists_request(mock_post, gist):
    """Properly pass gist request"""

    gist.get_gists()
    mock_post.assert_called_with(
        'https://api.github.com/users/testuser/gists',
        params=None
    )

    gist.get_gists(since=dt.datetime(2019, 1, 1, 10, 0, 20))
    mock_post.assert_called_with(
        'https://api.github.com/users/testuser/gists',
        params={'since': '2019-01-01T10:00:20Z'}
    )


def test_create_parser():
    parser = create_parser()
    args = parser.parse_args([
        '-g', '-u', 'test_user', '-t', 'path/to/token.txt', '-s', '2019-01-01 12:00:01'
    ])

    assert args.get is True
    assert args.username == 'test_user'
    assert args.token_file == 'path/to/token.txt'
    assert args.since == dt.datetime(2019, 1, 1, 12, 0, 1)

    args = parser.parse_args([
        '-u', 'test_user', '-t', 'path/to/token.txt', '-n', 'path/to/file.py', '-d', 'My gist'
    ])

    assert args.get is False
    assert args.username == 'test_user'
    assert args.token_file == 'path/to/token.txt'
    assert args.name[0] == 'path/to/file.py'
    assert args.description == 'My gist'
    assert args.since is None
