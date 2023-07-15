import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from semantic_version import SimpleSpec, Version

from ghastoolkit.octokit.octokit import OctoItem


def parseVersion(data: str) -> Version:
    stack = data.split(".")
    if len(stack) == 1:
        return Version(f"{data}.0.0")
    elif len(stack) == 2:
        return Version(f"{data}.0")
    return Version(data)


@dataclass
class AdvisoryAffect:
    """Advisory Affects"""

    ecosystem: str
    package: str

    range_events: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def loadAffect(data: dict) -> "AdvisoryAffect":
        range_events = {}

        adaff = AdvisoryAffect(
            data.get("package", {}).get("ecosystem", "NA").lower(),
            data.get("package", {}).get("name", "NA"),
            range_events=range_events,
        )
        return adaff

    def check(self, version: str) -> bool:
        """Check if version is in range"""
        if not version and not isinstance(version, Version):
            raise Exception(f"Not Version type")

        introduced = self.range_events.get("introduced")
        fixed = self.range_events.get("fixed")
        spec = SimpleSpec(f">={introduced},<={fixed}")
        return parseVersion(version) in spec

        # return version in spec


@dataclass
class Advisory(OctoItem):
    ghsa_id: str
    severity: str

    summary: Optional[str] = None
    url: Optional[str] = None

    cwes: List[str] = field(default_factory=list)

    affected: List[AdvisoryAffect] = field(default_factory=list)
    """Affected versions"""

    @staticmethod
    def loadAdvisory(path: str) -> "Advisory":
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


class Advisories:
    def __init__(self) -> None:
        self.advisories: List[Advisory] = []

    def append(self, advisory: Advisory):
        self.advisories.append(advisory)

    def __len__(self) -> int:
        return len(self.advisories)

    def loadAdvisory(self, path: str):
        """Load single advisory from file"""
        self.advisories.append(Advisory.loadAdvisory(path))

    def check(self, dependency: "Dependency") -> Optional[Advisory]:
        """Check if dependency is affected by any advisory"""

        return
