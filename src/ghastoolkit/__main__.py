import json
import os
import logging
import argparse

from ghastoolkit import __name__ as name, __banner__
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.helpers import *

MODES = {
    "codescanning-alerts": codeScanningAlerts,
    "dependencygraph": depGraph,
    "codeql-db-list": codeqlDatabaseList,
    "codeql-db-download": codeqlDatabaseDownload,
}

# Arguments
parser = argparse.ArgumentParser(name)
parser.add_argument("--debug", action="store_true")

parser.add_argument("mode", choices=["all", *MODES.keys()])

parser.add_argument("-sha", default=os.environ.get("GITHUB_SHA"), help="Commit SHA")
parser.add_argument("-ref", default=os.environ.get("GITHUB_REF"), help="Commit ref")

parser_github = parser.add_argument_group("GitHub")
parser_github.add_argument(
    "-r",
    "--github-repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser_github.add_argument(
    "--github-instance",
    default=os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
    help="GitHub Instance",
)
parser_github.add_argument(
    "-t",
    "--github-token",
    default=os.environ.get("GITHUB_TOKEN"),
    help="GitHub API Token",
)


if __name__ == "__main__":
    arguments = parser.parse_args()
    # logger
    logging.basicConfig(
        level=logging.DEBUG
        if arguments.debug or os.environ.get("DEBUG")
        else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # GitHub Init
    GitHub.init(
        repository=arguments.github_repository,
        instance=arguments.github_instance,
        token=arguments.github_token,
    )

    if not GitHub.repository:
        raise Exception(f"GitHub Repository must be set")

    for mode, mode_func in MODES.items():
        if mode == arguments.mode or arguments.mode == "all":
            logging.debug(f"Running Mode Function :: {mode}")
            mode_func(arguments)
