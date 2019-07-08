import argparse
import datetime as dt
from itertools import zip_longest
from pathlib import Path
import sys

from pygists import Pygists


def optional_date_type(s):
    try:
        return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except TypeError:
        return None


def create_parser():
    parser = argparse.ArgumentParser('Create or get GitHub gists.')
    parser.add_argument(
        '--username', '-u', help='GitHub username', required=True
    )
    parser.add_argument(
        '--token-file', '-t', help='Path to file containing GitHub OAuth token',
        required=True
    )
    parser.add_argument('--get', '-g', action='store_true', default=False, help='Only get gists')
    parser.add_argument(
        '--since', '-s', default=None, type=optional_date_type,
        help='Get gists since this date in YYYY-MM-DD HH:MM:SS format'
    )
    parser.add_argument(
        '--content', '-c', action='append', default=[],
        help=(
            'Gist content. All contents mapped 1-to-1 to names.'
            ' Ignored if name corresponds to existing files.'
        )
    )
    parser.add_argument(
        '--name', '-n', action='append', default=[],
        help=(
            'Gist file name. If a filename exists, will read contents from it,'
            ' otherwise all names mapped 1-to-1 to contents'
        )
    )
    parser.add_argument('--description', '-d', default='', help='Gist description')
    parser.add_argument(
        '--private', '-p', action='store_true', default=False,
        help='Make the gist private (default: False)'
    )

    return parser


def main():
    args = create_parser().parse_args()

    gist = Pygists(args.username, args.token_file)

    if args.get is True:

        gists = gist.get_gists(since=args.since)

        for gist in gists:
            gist.describe()
        sys.exit(0)

    names = []
    contents = []

    for name, content in zip_longest(args.name, args.content):
        names.append(name)

        if Path(name).exists() is True:
            with open(name, 'r') as f:
                contents.append(f.read())

        else:
            contents.append(content)

    new_gist = gist.create_gist(
        names=names, contents=contents, description=args.description,
        public=True if args.private is False else False
    )
    new_gist.describe()
