import json
import os
from typing import List, Optional
from dataclasses import dataclass, field

from semantic_version import SimpleSpec, Version

from ghastoolkit.octokit.octokit import OctoItem


def parseVersion(data: str) -> str:
    stack = data.split(".")
    if len(stack) == 1:
        return f"{data}.0.0"
    elif len(stack) == 2:
        return f"{data}.0"
    return data


@dataclass
class AdvisoryAffect:
    """Advisory Affected"""

    ecosystem: str
    """Ecosystem / Dependency Manager / PURL type"""
    package: str
    """Package Full Name ([namespace +] name"""

    introduced: Optional[str] = None
    """Introduced Version"""
    fixed: Optional[str] = None
    """Fixed Version"""

    package_dependency: Optional["Dependency"] = None

    def __post_init__(self):
        self.ecosystem = self.ecosystem.lower()
        # load package as dependency
        from ghastoolkit import Dependency

        # HACK can we do this a better way?
        if self.ecosystem in ["maven", "nuget"]:
            namespace, name = self.package.rsplit(".", 1)
        else:
            namespace = None
            name = self.package

        self.package_dependency = Dependency(name, namespace, manager="maven")

        if self.introduced:
            self.introduced = parseVersion(self.introduced)
        if self.fixed:
            self.fixed = parseVersion(self.fixed)

    @staticmethod
    def loadAffect(data: dict) -> "AdvisoryAffect":
        """Load affects from data

        https://github.com/github/advisory-database
        """
        # TODO
        adaff = AdvisoryAffect(
            data.get("package", {}).get("ecosystem", "NA").lower(),
            data.get("package", {}).get("name", "NA"),
        )
        return adaff

    def check(self, dependency: "Dependency") -> bool:
        """Check if version is in range"""

        from ghastoolkit import Dependency

        if not isinstance(dependency, Dependency):
            raise Exception(f"Unknown type provided :: {type(dependency)}")
        # None checks
        if not self.package_dependency or not dependency.version:
            return False
        # manager / ecosystem
        if dependency.manager != self.ecosystem:
            return False
        # name
        if dependency.name != self.package_dependency.name:
            return False
        return self.checkVersion(dependency.version)

    def checkVersion(self, version: str) -> bool:
        """Check version data with"""
        if not self.introduced or not self.fixed:
            return False
        # print(f"- {self.introduced} > {parseVersion(version)} < {self.fixed}")
        spec = SimpleSpec(f">={self.introduced},<{self.fixed}")
        return Version(parseVersion(version)) in spec


@dataclass
class Advisory(OctoItem):
    """GitHub Advisory"""

    ghsa_id: str
    """GitHub Security Advisory Identifier"""
    severity: str
    """Severity level"""

    summary: Optional[str] = None
    """Summary / Description of the advisory"""
    url: Optional[str] = None
    """Reference URL"""

    cwes: List[str] = field(default_factory=list)
    """List of CWEs"""

    affected: List[AdvisoryAffect] = field(default_factory=list)
    """Affected versions"""

    @staticmethod
    def loadAdvisory(path: str) -> "Advisory":
        """Load Advisory from path using GitHub Advisory Spec"""
        if not os.path.exists(path):
            raise Exception(f"Advisory path does not exist")

        with open(path, "r") as handle:
            data = json.load(handle)

        affected = []
        for affect in data.get("affected", []):
            affected.append(AdvisoryAffect.loadAffect(affect))

        advisory = Advisory(
            ghas_id=data.get("id", "NA"),
            severity=data.get("database_specific", {}).get("severity", "NA").lower(),
            summary=data.get("summary"),
            affected=affected,
        )
        return advisory

    def check(self, dependency: "Dependency") -> Optional["Advisory"]:
        """Check if dependency is affected by advisory"""
        for affect in self.affected:
            if affect.check(dependency):
                return self
        return


class Advisories(list):
    def loadAdvisory(self, path: str):
        """Load single advisory from file"""
        self.append(Advisory.loadAdvisory(path))

    def check(self, dependency: "Dependency") -> List[Advisory]:
        """Check if dependency is affected by any advisory"""
        results = []
        for a in self:
            result = a.check(dependency)
            if result:
                results.append(result)

        return results
