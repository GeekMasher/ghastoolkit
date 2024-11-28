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
        if self.subparser:
            # self.addModes([""])

            parser = self.parser.add_argument_group("billing")
            parser.add_argument(
                "--csv",
                help="Input CSV Billing File",
            )

    def run(self, arguments: Namespace):
        self.default_logger()

        if arguments.csv:
            logging.info(f"Loading GHAS Billing from {arguments.csv}")

            ghas = Billing.loadFromCsv(arguments.csv)
        else:
            if GitHub.token is None:
                logging.error("No GitHub Token provided")
                return
            org = Organization(GitHub.owner)
            billing = Billing(org)
            ghas = billing.getGhasBilling()

        if not ghas:
            logging.error("No GHAS Billing found")
            return

        print(f"GHAS Active Committers :: {ghas.active}")
        print(f"GHAS Maximum Committers :: {ghas.maximum}")
        print(f"GHAS Purchased Committers :: {ghas.purchased}")


if __name__ == "__main__":
    parser = BillingCommandLine("ghastoolkit-billing")
    parser.run(parser.parse_args())
    logging.info(f"Finished!")
