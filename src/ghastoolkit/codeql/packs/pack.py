"""CodeQL Packs."""

import os
import json
import glob
import logging
from typing import List, Optional
import yaml

from ghastoolkit.codeql.cli import CodeQL


logger = logging.getLogger("ghastoolkit.codeql.packs")


class CodeQLPack:
    """CodeQL Pack class."""

    codeql_packages: str = os.path.join(os.path.expanduser("~"), ".codeql", "packages")
    """CodeQL Packages Location"""

    def __init__(
        self, path: Optional[str] = None, cli: Optional[CodeQL] = None
    ) -> None:
        """Initialise CodeQL Pack."""
        self.cli = cli or CodeQL()

        self.path = path
        self.library = False
        self.name = ""
        self.version = ""
        self.dependencies = []

        if path:
            # if its a file
            if os.path.isfile(path) and path.endswith("qlpack.yml"):
                path = os.path.realpath(os.path.dirname(path))

            self.path = os.path.realpath(os.path.expanduser(path))
            self.load()

    @property
    def qlpack(self) -> str:
        """QL Pack Location."""
        if self.path:
            return os.path.join(self.path, "qlpack.yml")
        return "qlpack.yml"

    def validate(self) -> bool:
        """Validate and check if the path is a valid CodeQL Pack."""
        return os.path.exists(self.qlpack)

    def load(self):
        """Load QLPack file."""
        if not os.path.exists(self.qlpack):
            raise Exception(f"Failed to find qlpack file")

        logger.debug(f"Loading Pack from path :: {self.path}")
        with open(self.qlpack, "r") as handle:
            data = yaml.safe_load(handle)

        self.library = bool(data.get("library"))
        self.name = data.get("name", "")
        self.version = data.get("version", "")
        self.dependencies.extend(data.get("dependencies", []))

    def run(self, *args, display: bool = False) -> Optional[str]:
        """Run Pack command."""
        return self.cli.runCommand("pack", *args, display=display)

    def create(self) -> str:
        """Create / Compile a CodeQL Pack."""
        logger.debug(f"Creating CodeQL Pack :: {self.name}")
        home = os.path.expanduser("~")
        packages = os.path.join(home, ".codeql", "packages")
        self.run("create", "--output", packages, self.path)
        return os.path.join(packages, self.name, self.version)

    def publish(self):
        """Publish a CodeQL Pack to a remote registry."""
        self.run("publish", self.path)

    @staticmethod
    def download(name: str, version: Optional[str] = None) -> "CodeQLPack":
        """Download a CodeQL Pack."""
        cli = CodeQL()
        full_name = f"{name}@{version}" if version else name
        logger.debug(f"Download Pack :: {full_name}")

        cli.runCommand("pack", "download", full_name)
        base = os.path.join(CodeQLPack.codeql_packages, name)
        if version:
            return CodeQLPack(os.path.join(base, version))
        else:
            return CodeQLPack(glob.glob(f"{base}/**/")[0])

    def install(self, display: bool = False):
        """Install Dependencies for a CodeQL Pack."""
        self.run("install", self.path, display=display)

    def resolveQueries(self, suite: Optional[str] = None) -> List[str]:
        """Resolve all the queries in a Pack and return them."""
        results = []
        pack = f"{self.name}:{suite}" if suite else self.name
        result = self.cli.runCommand(
            "resolve", "queries", "--format", "bylanguage", pack
        )
        if result:
            for _, queries in json.loads(result).get("byLanguage", {}).items():
                results.extend(list(queries.keys()))
        return results

    @property
    def remote_version(self) -> Optional[str]:
        """Gets the remote version of the pack if possible."""
        from ghastoolkit import CodeScanning

        try:
            cs = CodeScanning()
            latest_remote = cs.getLatestPackVersion(self.name)
            latest_version = (
                latest_remote.get("metadata", {})
                .get("container", {})
                .get("tags", ["NA"])[0]
            )
            return latest_version
        except Exception:
            logging.debug(f"Error getting remote version")
        return None

    def __str__(self) -> str:
        """To String."""
        if self.name != "":
            return f"CodeQLPack('{self.name}', '{self.version}')"
        return f"CodeQLPack('{self.path}')"
