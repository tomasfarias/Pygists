import datetime as dt
import unittest.mock

import pytest

from pygists import Pygists


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
