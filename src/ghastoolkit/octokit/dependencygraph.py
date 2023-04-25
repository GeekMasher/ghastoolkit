import fnmatch
import logging
from dataclasses import dataclass, field
from datetime import datetime
import re
from ghastoolkit.octokit.github import GitHub, Repository

from ghastoolkit.octokit.octokit import GraphQLRequest, Optional, RestRequest

logger = logging.getLogger("ghastoolkit.octokit.dependencygraph")


@dataclass
class Dependency:
    name: str
    namespace: Optional[str] = None
    version: Optional[str] = None
    manager: Optional[str] = None
    path: Optional[str] = None
    qualifiers: dict[str, str] = field(default_factory=list)

    licence: Optional[str] = None

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

    @staticmethod
    def fromPurl(purl: str) -> "Dependency":
        dep = Dependency("")
        pkg, dep.version = purl.split("@", 1)

        if pkg.count("/") == 2:
            manager, dep.namespace, dep.name = pkg.split("/", 3)
        elif pkg.count("/") == 1:
            manager, dep.name = pkg.split("/", 2)
        elif pkg.count("/") > 2:
            manager, dep.namespace, dep.name = pkg.split("/", 2)
        else:
            raise Exception(f"Unable to parse PURL :: {purl}")

        _, dep.manager = manager.split(":", 1)

        return dep

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

    def findLicenses(self, licenses: list[str]) -> "Dependencies":
        """Find Denied License"""
        regex_list = [re.compile(name_filter) for name_filter in licenses]
        return Dependencies(
            [
                dep
                for dep in self
                if any(regex.search(dep.licence or "NA") for regex in regex_list)
            ]
        )

    def findNames(self, names: list[str]) -> "Dependencies":
        """Find by Name using wildcards"""
        regex_list = [re.compile(name_filter) for name_filter in names]
        return Dependencies(
            [dep for dep in self if any(regex.search(dep.name) for regex in regex_list)]
        )


class DependencyGraph:
    def __init__(self, repository: Optional[Repository] = None) -> None:
        self.repository = repository or GitHub.repository
        self.rest = RestRequest(repository)
        self.graphql = GraphQLRequest(repository)

    def getDependencies(self) -> Dependencies:
        """Get Dependencies from SBOM"""
        result = Dependencies()
        spdx_bom = self.exportBOM()

        for package in spdx_bom.get("sbom", {}).get("packages", []):
            extref = False
            dep = Dependency("")
            for ref in package.get("externalRefs", []):
                if ref.get("referenceType"):
                    dep = Dependency.fromPurl(ref.get("referenceLocator"))
                    extref = True

            if extref:
                dep.licence = package.get("licenseConcluded")
            else:
                manager, name = package.get("name", "").split(":")
                dep = Dependency(
                    name,
                    version=package.get("versionInfo"),
                    manager=manager,
                    licence=package.get("licenseConcluded"),
                )

            result.append(dep)

        return result

    def exportBOM(self) -> Dependencies:
        """Download / Export DependencyGraph SBOM"""
        return self.rest.get("/repos/{owner}/{repo}/dependency-graph/sbom")

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
