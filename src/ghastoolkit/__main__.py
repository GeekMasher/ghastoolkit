"""ghastoolkit main workflow."""
import logging
import os

from argparse import Namespace

from ghastoolkit import __name__ as name, __banner__, __version__
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.dependencygraph import (
    DependencyGraph,
)
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

    def set_modes(self) -> list[str]:
        super().set_modes()
        self.modes.extend(["all", "codescanning", "dependencygraph"])

    def run(self, arguments: Namespace):
        """Run main CLI."""
        if arguments.version:
            print(f"v{__version__}")
            return

        print(__banner__)

        # GitHub Init
        GitHub.init(
            repository=arguments.github_repository,
            instance=arguments.github_instance,
            token=arguments.github_token,
        )

        if not GitHub.repository:
            raise Exception(f"GitHub Repository must be set")
        logging.debug(f"Mode :: {arguments.mode}")


if __name__ == "__main__":
    # Arguments
    parser = MainCli(name)

    arguments = parser.parse_args()
    parser.run(arguments)
