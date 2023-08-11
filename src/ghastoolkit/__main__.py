"""ghastoolkit main workflow."""

from argparse import Namespace

from ghastoolkit import __name__ as name, __banner__, __version__
from ghastoolkit.codeql.__main__ import CodeQLCommandLine
from ghastoolkit.utils.cli import CommandLine
from ghastoolkit.supplychain.__main__ import SupplyChainCLI, runOrgAudit


def header(name: str):
    print("#" * 32)
    print(f"    {name}")
    print("#" * 32)
    print("")


class MainCli(CommandLine):
    """Main CLI."""

    def arguments(self):
        """Adding additional parsers from submodules."""
        SupplyChainCLI(name="supplychain", parser=self.parser)
        CodeQLCommandLine(name="codeql", parser=self.parser)

    def run(self, arguments: Namespace):
        """Run main CLI."""
        if arguments.version:
            print(f"v{__version__}")
            return

        print(__banner__)

        if arguments.mode == "org-audit":
            # supplychain
            runOrgAudit(arguments)
            return


if __name__ == "__main__":
    # Arguments
    parser = MainCli(name)

    parser.run(parser.parse_args())
