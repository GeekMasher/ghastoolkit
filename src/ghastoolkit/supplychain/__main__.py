"""Supply Chain Toolkit CLI."""
from argparse import ArgumentParser
import logging
import os

from yaml import parse

from ghastoolkit.octokit.dependencygraph import DependencyGraph
from ghastoolkit.octokit.github import GitHub

parser = ArgumentParser("ghastoolkit.supplychain")
parser.add_argument("--debug", action="store_true")
parser.add_argument("mode", choices=["org-audit"])
parser.add_argument("-r", "--repository", required=True)
parser.add_argument("-t", "--token", default=os.environ.get("GITHUB_TOKEN"))
parser.add_argument("--licenses", default="GPL-*,AGPL-*,LGPL-*")

arguments = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


GitHub.init(arguments.repository, token=arguments.token)
logging.info(f"GitHub :: `{GitHub.repository}`")

if arguments.mode == "org-audit":
    licenses = arguments.licenses.split(",")
    logging.info(f"Licenses :: {','.join(licenses)}")

    if arguments.debug:
        logging.getLogger("ghastoolkit.octokit.dependencygraph").setLevel(logging.DEBUG)

    depgraph = DependencyGraph()

    dependencies = depgraph.getOrganizationDependencies()

    for repo, deps in dependencies.items():
        # get a list of deps that match the licenses
        violations = deps.findLicenses(licenses)
        # get a list of deps with no license data
        unknowns = deps.findUnknownLicenses()

        if len(violations) == 0 and len(unknowns) == 0:
            continue

        logging.info(f" > {repo} :: {len(deps)}")
        logging.info(f" |-> Unknowns   :: {len(unknowns)}")
        for unknown in unknowns:
            logging.warning(f" |---> {unknown.getPurl()}")

        logging.info(f" |-> Violations :: {len(violations)}")
        for violation in violations:
            logging.warning(f" |---> {violation.getPurl()}")
