import logging
from dataclasses import dataclass, field
from typing import Optional, Union, Dict

from ghastoolkit.supplychain.dependencyalert import DependencyAlert
from ghastoolkit.octokit.github import Repository

logger = logging.getLogger("ghastoolkit.supplychain.dependency")


@dataclass
class Dependency:
    """Dependency."""

    name: str
    """Name of the Dependency"""
    namespace: Optional[str] = None
    """Namespace of the Dependency"""
    version: Optional[str] = None
    """Version of the Dependency"""
    manager: Optional[str] = None
    """Package Manager"""
    path: Optional[str] = None
    """Path to the Dependency"""
    qualifiers: dict[str, str] = field(default_factory=dict)
    """Qualifiers"""
    license: Optional[str] = None
    """License information"""
    alerts: list[DependencyAlert] = field(default_factory=list)
    """Security Alerts"""

    repository: Optional[Union[str, Repository]] = None
    """GitHub Repository for the dependency"""

    repositories: set[Repository] = field(default_factory=set)
    """List of repositories for the dependency"""

    def __post_init__(self):
        # normalize manager
        if self.manager:
            self.manager = self.manager.lower()
        if self.repository and isinstance(self.repository, str):
            self.repository = Repository.parseRepository(self.repository)

    def getPurl(self, version: bool = True) -> str:
        """Create a PURL from the Dependency.

        https://github.com/package-url/purl-spec
        """
        result = f"pkg:"
        if self.manager:
            result += f"{self.manager.lower()}/"
        if self.namespace:
            result += f"{self.namespace}/"
        result += f"{self.name}"
        if version and self.version:
            result += f"@{self.version}"

        return result

    @staticmethod
    def fromPurl(purl: str) -> "Dependency":
        """Create a Dependency from a PURL."""
        dep = Dependency("")
        # version (at end)
        if "@" in purl:
            pkg, dep.version = purl.split("@", 1)
        else:
            pkg = purl

        slashes = pkg.count("/")
        if slashes == 0 and pkg.count(":", 1):
            # basic purl `npm:name`
            manager, dep.name = pkg.split(":", 1)
        elif slashes == 2:
            manager, dep.namespace, dep.name = pkg.split("/", 3)
        elif slashes == 1:
            manager, dep.name = pkg.split("/", 2)
        elif slashes > 2:
            manager, dep.namespace, dep.name = pkg.split("/", 2)
        else:
            raise Exception(f"Unable to parse PURL :: {purl}")

        if manager.startswith("pkg:"):
            _, dep.manager = manager.split(":", 1)
        else:
            dep.manager = manager

        return dep

    @property
    def fullname(self) -> str:
        """Full Name of the Dependency."""
        if self.namespace:
            sep = "/"
            if self.manager == "maven":
                sep = ":"
            return f"{self.namespace}{sep}{self.name}"
        return self.name

    def __str__(self) -> str:
        """To String (PURL)."""
        return self.getPurl()

    def __repr__(self) -> str:
        return self.getPurl()

    def __hash__(self) -> int:
        return hash(self.getPurl())
