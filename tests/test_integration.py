import os
from typing import Optional
from unittest.mock import patch
import sys
import datetime as dt

import pytest

from pygists.cli import main
from pygists import Pygists


GITHUB_USER = os.getenv('GITHUB_USER', None)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)


pytestmark = pytest.mark.skipif(
    GITHUB_USER is None or GITHUB_TOKEN is None,
    reason='Must have GITHUB_USER and GITHUB_TOKEN environment variables set to run integration tests'
)

GIST = """msg = 'Merely a test gist, please delete me!'
print(msg)
"""


@pytest.fixture(scope='function')
def gist(tmpdir):
    p = tmpdir.mkdir('gist').join('gist.py')
    p.write(GIST)
    return p


def get_created_gist_id_by_description(description: str) -> Optional[str]:
    pygists = Pygists(os.getenv('GITHUB_USER', None), os.getenv('GITHUB_TOKEN', None))
    gists = pygists.list_user_gists()

    for gist in gists:
        if gist.description == description:
            return gist.id
    return None


@patch.dict(os.environ, {'GITHUB_USER': GITHUB_USER, 'GITHUB_TOKEN': GITHUB_TOKEN})
@pytest.mark.integration
def test_creating_a_gist(gist, capsys):
    args = [
        'pygists', 'create', str(gist), '-d', 'This is the description of a test gist!', '--show-content'
    ]
    with patch.object(sys, 'argv', args):
        main()

    captured = capsys.readouterr()
    assert 'Merely a test gist, please delete me!' in captured.out
    assert 'This is the description of a test gist!' in captured.out
    assert 'gist.py' in captured.out
    created_id = get_created_gist_id_by_description('This is the description of a test gist!')
    assert created_id is not None


@patch.dict(os.environ, {'GITHUB_USER': GITHUB_USER, 'GITHUB_TOKEN': GITHUB_TOKEN})
@pytest.mark.integration
def test_list_all_users_gists(capsys):
    args = [
        'pygists', 'ls', '--since', (dt.datetime.now() - dt.timedelta(days=1)).isoformat(),
        '--show-content'
    ]
    with patch.object(sys, 'argv', args):
        main()

    captured = capsys.readouterr()
    assert 'This is the description of a test gist!' in captured.out
    assert 'gist.py' in captured.out
    created_id = get_created_gist_id_by_description('This is the description of a test gist!')
    assert created_id in captured.out


@patch.dict(os.environ, {'GITHUB_USER': GITHUB_USER, 'GITHUB_TOKEN': GITHUB_TOKEN})
@pytest.mark.integration
def test_deleting_a_gist(capsys):
    gist_id = get_created_gist_id_by_description('This is the description of a test gist!')
    args = [
        'pygists', 'delete', gist_id,
    ]
    with patch.object(sys, 'argv', args):
        main()

    captured = capsys.readouterr()
    assert f'Deleted gist: {gist_id}' in captured.out
    created_id = get_created_gist_id_by_description('This is the description of a test gist!')
    assert created_id is None
