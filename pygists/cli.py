import argparse
import datetime as dt
import sys
import os

from pygists import Pygists
from pygists import handlers


def optional_date_type(s):
    try:
        return dt.datetime.fromisoformat(s)
    except TypeError:
        return None


def create_parser():
    parser = argparse.ArgumentParser('Create or get GitHub gists.')
    subparsers = parser.add_subparsers(help='List, create, get, update or delete gists', dest='subcommand')

    parse_ls = subparsers.add_parser('ls', help='List all gists')
    parse_ls.add_argument(
        '--since', '-s', default=None, type=optional_date_type,
        help='Get gists since this date in ISO 8601 format'
    )
    add_common_arguments(parse_ls)

    parse_get = subparsers.add_parser('get', help='Get a gist')
    parse_get.add_argument(
        'id', help='The gist ID to get'
    )
    add_common_arguments(parse_get)

    parse_delete = subparsers.add_parser('delete', help='Delete a gist')
    parse_delete.add_argument(
        'id', help='The gist ID to delete'
    )
    add_common_arguments(parse_delete)

    parse_update = subparsers.add_parser('update', help='Update a gist')
    parse_update.add_argument(
        'id', help='The gist ID to update'
    )
    parse_update.add_argument(
        '--add', nargs='+', default=[], required=False,
        help='One or more files to be added to the gist'
    )
    parse_update.add_argument(
        '--delete', nargs='+', default=[], required=False,
        help='One or more files to be deleted from the gist'
    )
    parse_update.add_argument(
        '--modify', nargs='+', default=[], required=False,
        help='One or more files to be modified from the gist formatted as OLD_NAME=path/to/new.file'
    )
    parse_update.add_argument(
        '--description', '-d', required=False, help='The new gist description'
    )
    add_common_arguments(parse_update)

    parse_create = subparsers.add_parser('create', help='Create a new gist')
    parse_create.add_argument(
        'file', nargs='+', help='One or more files to be set to the gist'
    )
    parse_create.add_argument(
        '--description', '-d', required=False, help='The gist description'
    )
    parse_create.add_argument(
        '--private', required=False, help='Make the gist private', default=False
    )
    add_common_arguments(parse_create)

    return parser


def add_common_arguments(parser):
    parser.add_argument(
        '--username', '-u', help='GitHub username',
        required=False, default=os.getenv('GITHUB_USER')
    )
    parser.add_argument(
        '--token', '-t', help='GitHub OAuth token',
        required=False, default=os.getenv('GITHUB_TOKEN')
    )
    parser.add_argument(
        '--json', default=False, action='store_true', help='Print gist in JSON format'
    )
    parser.add_argument(
        '--show-content', '-c', default=False, action='store_true', help="Show the gist's content",
    )
    return parser


def main():
    parsed = create_parser().parse_args(sys.argv[1:])
    pygists = Pygists(parsed.username, parsed.token)

    handler = getattr(handlers, parsed.subcommand)
    if handler is None:
        sys.exit(f'No handler defined for subcommand \'{parsed.subcommand}\'')

    handler(pygists, parsed)
