import json
import os
import logging
import argparse

from ghastoolkit import __name__ as name
from ghastoolkit.codeql import CodeQLDatabase
from ghastoolkit.codeql.databases import CodeQLDatabaseList
from ghastoolkit.octokit import dependencygraph
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.dependencygraph import (
    Dependencies,
    DependencyGraph,
    Dependency,
)

# Arguments
parser = argparse.ArgumentParser(name)
parser.add_argument("--debug", action="store_true")

parser.add_argument("mode", choices=["codescanning", "codeql", "dependencygraph"])

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
    default=os.environ.get("GITHUB_API_URL", "https://api.github.com"),
    help="GitHub Instance",
)
parser_github.add_argument(
    "-t",
    "--github-token",
    default=os.environ.get("GITHUB_TOKEN"),
    help="GitHub API Token",
)

arguments = parser.parse_args()


def header(name: str):
    print("#" * 32)
    print(f"    {name}")
    print("#" * 32)


# logger
logging.basicConfig(
    level=logging.DEBUG if arguments.debug or os.environ.get("DEBUG") else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# GitHub Init
GitHub.init(repository=arguments.github_repository, token=arguments.github_token)


if arguments.mode == "codescanning":
    header("Code Scanning")
    codescanning = CodeScanning(GitHub.repository)

    alerts = codescanning.getAlerts()

    print(f"Total Alerts :: {len(alerts)}")

elif arguments.mode == "dependencygraph":
    header("Dependency Graph")

    depgraph = DependencyGraph(GitHub.repository)
    bom = depgraph.exportBOM()
    packages = bom.get("sbom", {}).get("packages", [])

    print(f"Total Dependencies :: {len(packages)}")

    info = bom.get("sbom", {}).get("creationInfo", {})
    print(f"Created :: {info.get('created')}")

    print("\nTools:")
    for tool in info.get("creators", []):
        print(f" - {tool}")
