"""ghastoolkit main workflow."""

from argparse import Namespace
import logging

from ghastoolkit import __name__ as name, __banner__, __version__
from ghastoolkit.codeql.__main__ import CodeQLCommandLine
from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.dependencygraph import DependencyGraph
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.utils.cli import CommandLine
from ghastoolkit.supplychain.__main__ import (
    SupplyChainCLI,
    runOrgAudit as runSCOrgAudit,
)


def header(name: str, width: int = 32):
    print("#" * width)
    print(f"{name:^32}")
    print("#" * width)
    print("")


def runCodeScanning(arguments):
    codescanning = CodeScanning(GitHub.repository)

    alerts = codescanning.getAlerts()

    print(f"Total Alerts :: {len(alerts)}")

    analyses = codescanning.getLatestAnalyses(GitHub.repository.reference)
    print(f"\nTools:")

    for analyse in analyses:
        tool = analyse.get("tool", {}).get("name")
        version = analyse.get("tool", {}).get("version")
        created_at = analyse.get("created_at")

        print(f" - {tool} v{version} ({created_at})")


def runDependencyGraph(arguments):
    depgraph = DependencyGraph(GitHub.repository)
    bom = depgraph.exportBOM()
    packages = bom.get("sbom", {}).get("packages", [])

    print(f"Total Dependencies :: {len(packages)}")

    info = bom.get("sbom", {}).get("creationInfo", {})
    print(f"Created :: {info.get('created')}")

    print("\nTools:")
    for tool in info.get("creators", []):
        print(f" - {tool}")


class MainCli(CommandLine):
    """Main CLI."""

    def arguments(self):
        """Adding additional parsers from submodules."""
        self.addModes(["all"])

    def run(self, arguments: Namespace):
        """Run main CLI."""
        if arguments.version:
            print(f"v{__version__}")
            return

        print(__banner__)

        if arguments.mode in ["all", "codescanning"]:
            print("")
            header("Code Scanning")
            runCodeScanning(arguments)

        if arguments.mode in ["all", "dependencygraph"]:
            print("")
            header("Dependency Graph")
            runDependencyGraph(arguments)

        if arguments.mode == "org-audit":
            # run org audit with all products
            # supplychain
            runSCOrgAudit(arguments)
            return


if __name__ == "__main__":
    # Arguments
    parser = MainCli(name)

    parser.run(parser.parse_args())
