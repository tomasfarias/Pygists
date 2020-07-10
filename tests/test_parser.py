import datetime as dt

from pygists.cli import create_parser


def test_parse_ls_command():
    parser = create_parser()
    args = parser.parse_args([
        'ls', '-s', '2019-01-01T12:00:01', '-u', 'test_user', '-t', 'test_token'
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


def test_parse_delete_command():
    parser = create_parser()
    args = parser.parse_args([
        'delete', '1a2b3c4d5e6f', '-u', 'test_user', '-t', 'test_token',
    ])

    assert args.subcommand == 'delete'
    assert args.username == 'test_user'
    assert args.token == 'test_token'
    assert args.id == '1a2b3c4d5e6f'
