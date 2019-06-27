import argparse
import datetime as dt
from itertools import zip_longest
import os
from pathlib import Path
import sys
from typing import List, Dict, Iterable, Union
from urllib.parse import urljoin

import requests

from models.gist import Gist


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
			self, names: Iterable[str], contents: Iterable[str], description: str, public: bool
		) -> Dict:
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


	def get_gists(self, since: dt.datetime=None) -> List:
		"""Get all user's public gists"""
		endpoint = urljoin(BASE_ENDPOINT, f'users/{self.username}/gists')

		r = self.session.get(
			endpoint,
			params={'since': since.strftime('%Y-%m-%dT%H:%M:%SZ')} if since is not None else None
		)
		return [Gist.from_response(gist) for gist in r.json()]


	def get_or_create_gist(
			self, names: Iterable[str], contents: Iterable[str], description: str, public: bool
		) -> Union[Dict, List]:
		"""Get all gists, check if a gist exists with given file names and create it if it doesn't"""

		if len(names) != len(contents):
			raise ValueError('Length of names and contents differs.')

		current_gists = self.get_gists()

		for gist in current_gists:
			if sorted(gist['files'].keys()) == sorted(names):
				return gist

		return self.create_gist(names, contents, description, public)


if __name__ == '__main__':
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
		'--since', '-s', default=None, help='Get gists since this date in YYYY-MM-DD HH:MM:SS format'
	)
	parser.add_argument(
		'--content', '-c', action='append', default=[],
		help='Gist content. All contents mapped 1-to-1 to names. Ignored if name corresponds to existing files.'
	)
	parser.add_argument(
		'--name', '-n', action='append', default=[],
		help='Gist file name. If a filename exists, will read contents from it, otherwise all names mapped 1-to-1 to contents',
	)
	parser.add_argument('--description', '-d', help='Gist description')
	parser.add_argument(
		'--private', '-p', action='store_true', default=False, help='Make the gist private (default: False)'
	)

	args = parser.parse_args()

	gist = Pygists(args.username, args.token_file)

	if args.get is True:
		try:
			since = dt.datetime.strptime(args.since, '%Y-%m-%d %H:%M:%S')
		except TypeError:
			since = None

		gists = gist.get_gists(since=since)

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

