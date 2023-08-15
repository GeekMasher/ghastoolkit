"""CodeQL CLI for ghastoolkit."""
import logging
from argparse import Namespace
from ghastoolkit.codeql.cli import CodeQL
from ghastoolkit.codeql.packs.pack import CodeQLPack
from ghastoolkit.utils.cli import CommandLine


def codeqlPackPublish(arguments: Namespace):
    if not arguments.pack or arguments.pack == "":
        logging.error(f"CodeQL Pack path must be provided")
        exit(1)

    pack = CodeQLPack(arguments.pack)
    # logging.info(f"CodeQL Pack :: {pack}")

    remote = pack.remote_version

    if pack.version != remote:
        logging.info("Publishing CodeQL Pack...")
        pack.publish()
        logging.info(f"CodeQL Pack published :: {pack}")
    else:
        logging.info(f"CodeQL Pack is up to date :: {pack}")


class CodeQLCommandLine(CommandLine):
    """CodeQL CLI."""

    def arguments(self):
        """CodeQL arguments."""
        if self.subparser:
            self.addModes(["init", "analyze", "update", "pack-publish"])

            parser = self.parser.add_argument_group("codeql")
            parser.add_argument("-b", "--binary")
            parser.add_argument("-c", "--command", type=str)
            parser.add_argument("--pack", type=str, help="CodeQL Pack Path")

    def run(self, arguments: Namespace):
        codeql = CodeQL()

        if not codeql.exists():
            logging.error(f"Failed to find codeql on system")
            exit(1)

        logging.info(f"Found codeql on system :: '{' '.join(codeql.path_binary)}'")

        if arguments.mode == "pack-publish":
            codeqlPackPublish(arguments)


if __name__ == "__main__":
    parser = CodeQLCommandLine("ghastoolkit-codeql")
    parser.run(parser.parse_args())
    logging.info(f"Finished!")
