import logging
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime
from ghastoolkit.octokit.github import Repository

from ghastoolkit.octokit.octokit import Optional, RestRequest

logger = logging.getLogger("ghastoolkit.octokit.dependencygraph")


@dataclass
class Dependency:
    name: str
    namespace: Optional[str] = None
    version: Optional[str] = None
    manager: Optional[str] = None
    path: Optional[str] = None
    qualifiers: dict[str, str] = field(default_factory=list)

    def getPurl(self) -> str:
        """Get PURL
        https://github.com/package-url/purl-spec
        """
        result = f"pkg:"
        if self.manager:
            result += f"{self.manager}/"
        if self.namespace:
            result += f"{self.namespace}/"
        result += f"{self.name}"
        if self.version:
            result += f"@{self.version}"

        return result

    def __str__(self) -> str:
        return self.getPurl()

    def __repr__(self) -> str:
        return self.getPurl()


class Dependencies(list[Dependency]):
    def exportBOM(
        self,
        tool: str,
        path: str,
        sha: str = "",
        ref: str = "",
        version: str = "0.0.0",
        url: str = "",
    ) -> dict:
        """Create a dependency graph submission JSON payload for GitHub"""
        resolved = {}
        for dep in self:
            name = dep.name
            purl = dep.getPurl()
            resolved[name] = {"package_url": purl}

        data = {
            "version": 0,
            "sha": sha,
            "ref": ref,
            "job": {"correlator": tool, "id": tool},
            "detector": {"name": tool, "version": version, "url": url},
            "scanned": datetime.now().isoformat(),
            "manifests": {
                tool: {
                    "name": tool,
                    "file": {
                        "source_location": path,
                    },
                    "resolved": resolved,
                }
            },
        }
        return data


class DependencyGraph:
    def __init__(self, repository: Repository) -> None:
        self.rest = RestRequest(repository)

    def exportBOM(self) -> dict:
        bom = self.rest.get("/repos/{owner}/{repo}/dependency-graph/sbom")
        return bom

    def submitDependencies(
        self,
        dependencies: Dependencies,
        tool: str,
        path: str,
        sha: str = "",
        ref: str = "",
        version: str = "0.0.0",
        url: str = "",
    ):
        """
        https://docs.github.com/en/rest/dependency-graph/dependency-submission?apiVersion=2022-11-28#create-a-snapshot-of-dependencies-for-a-repository
        """
        self.rest.postJson(
            "/repos/{owner}/{repo}/dependency-graph/snapshots",
            dependencies.exportBOM(tool, path, sha, ref, version, url),
            expected=201,
        )
