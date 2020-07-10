"""Subcommand handlers"""
from pygists import Pygists


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


def delete(pygists: Pygists, args):
    pygists.delete_gist(args.id)
    print(f'Deleted gist: {args.id}')


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
