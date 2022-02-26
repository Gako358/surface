#!/home/user/path/to/surface/.venv/bin/python

import sys
import argparse

from pygit import Pygit as pg
from confup import push, pull, install

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Sync all repors local and remote
    parser_update = subparsers.add_parser("sync", help="Sync local and remote repos")

    # push and pull local and remote config files
    parser_push = subparsers.add_parser("push", help="Push local cfg files to commit changes")
    parser_pull = subparsers.add_parser("pull", help="Pull remote files and update local")
    parser_install = subparsers.add_parser("install", help="Setup all config files")
    
    parser_update.set_defaults(func=pg.run) 

    parser_push.set_defaults(func=push)
    parser_pull.set_defaults(func=pull)
    parser_install.set_defaults(func=install)

    options = parser.parse_args()
    options.func(options)

if __name__ == "__main__":
    main()
