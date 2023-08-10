import logging
import os
from argparse import ArgumentParser, Namespace
from typing import Optional


class CommandLine:
    def __init__(
        self,
        name: Optional[str] = None,
        default_logger: bool = True,
    ) -> None:
        self.parser = ArgumentParser(name or "ghastoolkit")
        self.default()
        self.arguments()

        self.modes = ["default"]
        self.set_modes()

        if default_logger:
            self.default_logger()

    def default(self):
        """Setup default arguments."""
        self.parser.add_argument("--debug", action="store_true")
        self.parser.add_argument("--version", action="store_true")

        github = self.parser.add_argument_group("github")

        github.add_argument(
            "-r",
            "--github-repository",
            dest="repository",
            default=os.environ.get("GITHUB_REPOSITORY"),
            help="GitHub Repository (default: GITHUB_REPOSITORY)",
        )
        github.add_argument(
            "--github-instance",
            dest="instance",
            default=os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
            help="GitHub Instance URL (default: GITHUB_SERVER_URL)",
        )
        github.add_argument(
            "-t",
            "--github-token",
            dest="token",
            default=os.environ.get("GITHUB_TOKEN"),
            help="GitHub API Token (default: GITHUB_TOKEN)",
        )

        github.add_argument(
            "-sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA"
        )
        github.add_argument(
            "-ref", default=os.environ.get("GITHUB_REF"), help="Commit ref"
        )

    def set_modes(self):
        """Set modes."""
        return []

    def arguments(self):
        """Set custom arguments."""
        return

    def run(self, arguments: Optional[Namespace] = None):
        """Run CLI."""
        raise Exception("Not implemented")

    def default_logger(self):
        """Setup default logger."""
        arguments = self.parse_args()
        logging.basicConfig(
            level=logging.DEBUG
            if arguments.debug or os.environ.get("DEBUG")
            else logging.INFO,
            format="%(message)s",
        )

    def parse_args(self) -> Namespace:
        """Parse arguments."""
        self.parser.add_argument(
            "mode", const="default", nargs="?", default="default", choices=self.modes
        )
        return self.parser.parse_args()
