"""ghastoolkit main workflow."""
import logging
import os

from argparse import Namespace

from ghastoolkit import __name__ as name, __banner__, __version__
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.utils.cli import CommandLine
from ghastoolkit.supplychain.__main__ import SupplyChainCLI


def header(name: str):
    print("#" * 32)
    print(f"    {name}")
    print("#" * 32)
    print("")


class MainCli(CommandLine):
    def arguments(self):
        super().arguments()

    def run(self, arguments: Namespace):
        """Run main CLI."""
        if arguments.version:
            print(f"v{__version__}")
            return

        print(__banner__)

        if not GitHub.repository:
            raise Exception(f"GitHub Repository must be set")


if __name__ == "__main__":
    # Arguments
    parser = MainCli(name)

    parser.run(parser.parse_args())
