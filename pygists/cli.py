import argparse
import datetime as dt
import sys
import os

from pygists import Pygists


def optional_date_type(s):
    try:
        return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except TypeError:
        return None


def create_parser():
    parser = argparse.ArgumentParser('Create or get GitHub gists.')
    subparsers = parser.add_subparsers(help='List, get, update or delete gists', dest='subcommand')

    parse_ls = subparsers.add_parser('ls', help='List all gists')
    parse_ls.add_argument(
        '--since', '-s', default=None, type=optional_date_type,
        help='Get gists since this date in YYYY-MM-DD HH:MM:SS format'
    )
    add_common_arguments(parse_ls)

    parse_get = subparsers.add_parser('get', help='Get a gist')
    parse_get.add_argument(
        'id', help='The gist ID to get'
    )
    add_common_arguments(parse_get)

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
    add_common_arguments(parse_create)

    return parser


def add_common_arguments(parser):
    parser.add_argument(
        '--username', '-u', help='GitHub username', required=True
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
    args = create_parser().parse_args(sys.argv[1:])
    pygists = Pygists(args.username, args.token)

    HANDLERS.get(args.subcommand, sys.exit(1))(pygists, args)
    sys.exit(0)


def get(pygists: Pygists, args):
    gist = pygists.get_gist(gist_id=args.id)
    gist.describe(as_json=args.json, show_content=args.show_content)


def ls(pygists: Pygists, args):
    gists = pygists.list_user_gists(since=args.since)

    for gist in gists:
        gist.describe(as_json=args.json, show_content=args.show_content)


def create(pygists: Pygists, args):
    gist = pygists.create_gist_from_files(
        *args.file, description=args.description, public=not args.private
    )
    gist.describe(as_json=args.json, show_content=args.show_content)


def update(pygists: Pygists, args):
    to_modify = {}
    for arg in args.to_modify:
        old_name, new_file = arg.split('=')
        to_modify[old_name] = new_file

    gist = pygists.edit_gist_from_files(
        gist_id=args.id, to_add=args.add, to_delete=args.delete,
        to_modify=to_modify, description=args.description
    )
    gist.describe(as_json=args.json, show_content=args.show_content)


HANDLERS = {
    'ls': ls,
    'get': get,
    'update': update,
    'create': create,
}
