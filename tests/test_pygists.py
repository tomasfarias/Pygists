import datetime as dt
import unittest.mock

import pytest

from pygists import Pygists
from pygists.cli import create_parser


@pytest.fixture
def gist():
    return Pygists('test_user', 'test_token')


def test_pygist_init(gist):
    assert gist.session.auth == ('test_user', 'test_token')


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
def test_list_gists_request(mock_get, gist):
    """Properly pass gist request"""

    gist.list_user_gists()
    mock_get.assert_called_with(
        'https://api.github.com/users/test_user/gists',
        params=None
    )

    gist.list_user_gists(since=dt.datetime(2019, 1, 1, 10, 0, 20))
    mock_get.assert_called_with(
        'https://api.github.com/users/test_user/gists',
        params={'since': '2019-01-01T10:00:20Z'}
    )


@unittest.mock.patch('requests.Session.patch')
def test_edit_gist_request(mock_patch, gist):
    """Properly pass gist edit request"""
    files = {
        'test.py': {'content': 'print("Hello World!")'},
        'test2.py': {'content': 'print("New Hello World!")', 'filename': 'new_test.py'},
        'test_delete.py': None,
    }
    gist.edit_gist(
        gist_id='1a2b3c4d5e6f', files=files, new_description='New Testing'
    )

    mock_patch.assert_called_with(
        'https://api.github.com/gists/1a2b3c4d5e6f',
        json={
            'files': {
                'test2.py': {'content': 'print("New Hello World!")', 'filename': 'new_test.py'},
                'test.py': {'content': 'print("Hello World!")'},
                'test_delete.py': None,
            },
            'description': 'New Testing'
        }
    )


def test_parse_ls_command():
    parser = create_parser()
    args = parser.parse_args([
        'ls', '-s', '2019-01-01 12:00:01', '-u', 'test_user', '-t', 'test_token'
    ])

    assert args.subcommand == 'ls'
    assert args.username == 'test_user'
    assert args.token == 'test_token'
    assert args.since == dt.datetime(2019, 1, 1, 12, 0, 1)


def test_parse_create_command():
    parser = create_parser()
    args = parser.parse_args([
        'create', 'path/to/file.py', 'path/to/another_file.py',
        '-d', 'My gist', '-u', 'test_user', '-t', 'test_token',
    ])

    assert args.subcommand == 'create'
    assert args.username == 'test_user'
    assert args.token == 'test_token'
    assert args.file == ['path/to/file.py', 'path/to/another_file.py']
    assert args.description == 'My gist'


def test_parse_get_command():
    parser = create_parser()
    args = parser.parse_args([
        'get', '1a2b3c4d5e6f', '--json', '-u', 'test_user', '-t', 'test_token',
    ])

    assert args.subcommand == 'get'
    assert args.username == 'test_user'
    assert args.token == 'test_token'
    assert args.id == '1a2b3c4d5e6f'
    assert args.json is True
    assert args.show_content is False


def test_parse_update_command():
    parser = create_parser()
    args = parser.parse_args([
        'update', '1a2b3c4d5e6f', '--add', 'path/to/file.py', 'path/to/another_file.py',
        '--modify', 'old_name.py=path/to/new_file.py',
        '--delete', 'delete_file.py', 'delete_file2.py',
        '-u', 'test_user', '-t', 'test_token',
    ])

    assert args.subcommand == 'update'
    assert args.username == 'test_user'
    assert args.token == 'test_token'
    assert args.id == '1a2b3c4d5e6f'
    assert args.add == ['path/to/file.py', 'path/to/another_file.py']
    assert args.modify == ['old_name.py=path/to/new_file.py']
    assert args.delete == ['delete_file.py', 'delete_file2.py']
