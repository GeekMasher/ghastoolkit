"""GitHub CodeQL Packs CLI."""
import os
import logging
from argparse import ArgumentParser
from ghastoolkit import __banner__
from ghastoolkit.codeql.packs.packs import CodeQLPacks
from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.github import GitHub

logging.basicConfig(level=logging.INFO, format="%(message)s")

parser = ArgumentParser("ghastoolkit.codeql.packs")
parser.add_argument(
    "--repository",
    default=os.environ.get("GITHUB_REPOSITORY"),
    help="GitHub Repository",
)
parser.add_argument("-r", "--remote", action="store_true", help="Enable remote mode")
parser.add_argument("-p", "--packs-path", default=os.getcwd(), help="Packs Path")
parser.add_argument(
    "-dd", "--display-dependencies", action="store_true", help="Display Dependencies"
)

arguments = parser.parse_args()
remote = True if arguments.repository else False

logging.info(__banner__)

if remote:
    GitHub.init(arguments.repository)
else:
    logging.warning(f"Repository not set, all remote activities are disabled")

code_scanning = CodeScanning()


logging.debug(f"Loading packs from environment...")

packs = CodeQLPacks()
packs.load(arguments.packs_path)

logging.info(f"CodeQL Packs :: {len(packs)}")
logging.info("")

for pack in packs:
    logging.info(f" - {pack}")

    if remote:
        remote_version = pack.remote_version
        if remote_version:
            logging.info(f"   |> Remote Version: `{pack.remote_version}`")

    if arguments.display_dependencies:
        logging.info(f"   |> Dependencies")
        for dep in pack.dependencies:
            logging.info(f"   |--> {dep}")
