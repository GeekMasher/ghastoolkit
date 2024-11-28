"""CodeQL CLI for ghastoolkit."""

import logging
from argparse import Namespace
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.enterprise import Organization
from ghastoolkit.octokit.billing import Billing
from ghastoolkit.utils.cli import CommandLine


class BillingCommandLine(CommandLine):
    """Billing CLI."""

    def arguments(self):
        """Billing arguments."""

    def run(self, arguments: Namespace):
        self.default_logger()

        if GitHub.token is None:
            logging.error("No GitHub Token provided")
            return

        org = Organization(GitHub.owner)
        print(f"Organization :: {org}")

        repos = org.getRepositories()
        print(f"Repositories :: {len(repos)}")

        billing = Billing(org)

        ghas = billing.getGhasBilling()

        print(f"GHAS Active Committers :: {ghas.active}")
        print(f"GHAS Maximum Committers :: {ghas.maximum}")
        print(f"GHAS Purchased Committers :: {ghas.purchased}")



if __name__ == "__main__":
    parser = BillingCommandLine("ghastoolkit-billing")
    parser.run(parser.parse_args())
    logging.info(f"Finished!")
