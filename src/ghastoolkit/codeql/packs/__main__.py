"""GitHub CodeQL Packs CLI."""
import os
import logging
from argparse import Namespace
from typing import Optional
from ghastoolkit.codeql.packs.packs import CodeQLPacks
from ghastoolkit.utils.cli import CommandLine


def codeqlPackPublish(arguments: Namespace, packs: CodeQLPacks):
    if not arguments.packs or arguments.packs == "":
        logging.error(f"CodeQL Pack path must be provided")
        exit(1)

    for pack in packs:
        remote = pack.remote_version
        logging.info(f"CodeQL Pack Remote Version :: {remote}")

        if pack.version != remote:
            logging.info("Publishing CodeQL Pack...")
            pack.publish()
            logging.info(f"CodeQL Pack published :: {pack}")
        else:
            logging.info(f"CodeQL Pack is up to date :: {pack}")


class CodeQLPacksCommandLine(CommandLine):
    def arguments(self):
        self.addModes(["publish", "queries", "version"])
        default_pack_path = os.path.expanduser("~/.codeql/packages")

        parser = self.parser.add_argument_group("codeql-packs")
        parser.add_argument(
            "--packs",
            type=str,
            default=os.environ.get("CODEQL_PACKS_PATH", default_pack_path),
            help="CodeQL Packs Path",
        )
        parser.add_argument(
            "--bump",
            type=str,
            default="patch",
            help="CodeQL Pack Version Bump",
        )

    def run(self, arguments: Optional[Namespace] = None):
        if not arguments:
            arguments = self.parse_args()

        logging.info(f"CodeQL Packs Path :: {arguments.packs}")
        packs = CodeQLPacks(arguments.packs)

        if arguments.mode == "publish":
            codeqlPackPublish(arguments, packs)

        elif arguments.mode == "version":
            logging.info(f"Loading packs from :: {arguments.packs}")

            for pack in packs:
                old_version = pack.version
                pack.updateVersion(arguments.bump)
                pack.updatePack()
                logging.info(
                    f"CodeQL Pack :: {pack.name} :: {old_version} -> {pack.version}"
                )
        else:
            # list packs
            logging.info(f"Loading packs from :: {arguments.packs}")
            for pack in packs:
                logging.info(f"CodeQL Pack :: {pack}")

                if not pack.library:
                    queries = pack.resolveQueries()
                    logging.info(f"Queries: {len(queries)}")
                    for query in queries:
                        logging.info(f"- {query}")


if __name__ == "__main__":
    parser = CodeQLPacksCommandLine("ghastoolkit-codeql-packs")
    parser.run(parser.parse_args())
    logging.info(f"Finished!")
