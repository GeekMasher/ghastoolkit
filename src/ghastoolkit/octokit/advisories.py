"""GitHub Security Advisories API."""
from typing import Optional
from ghastoolkit.octokit.github import GitHub, Repository
from ghastoolkit.octokit.octokit import RestRequest
from ghastoolkit.supplychain.advisories import Advisories, Advisory


class SecurityAdvisories:
    """Security Advisories."""

    def __init__(self, repository: Optional[Repository] = None) -> None:
        """Security Advisories REST API.

        https://docs.github.com/en/rest/security-advisories/repository-advisories
        """
        self.repository = repository or GitHub.repository
        if not self.repository:
            raise Exception("SecurityAdvisories requires Repository to be set")
        self.rest = RestRequest(self.repository)

    def getAdvisories(self) -> Advisories:
        """Get list of security advisories from a repository."""
        results = self.rest.get(
            "/repos/{owner}/{repo}/security-advisories", authenticated=True
        )
        if isinstance(results, list):
            advisories = Advisories()
            for advisory in results:
                aliases = []

                if advisory.get("cve_id"):
                    aliases.append(advisory.get("cve_id"))

                advisories.append(
                    Advisory(
                        ghsa_id=advisory.get("ghsa_id"),
                        severity=advisory.get("severity"),
                        aliases=aliases,
                        summary=advisory.get("summary"),
                        cwes=advisory.get("cwe_ids", []),
                    )
                )
            return advisories
        raise Exception(f"Error getting advisories from repository")

    def getAdvisory(self, ghsa_id: str) -> Advisory:
        """Get advisory by ghsa id."""
        result = self.rest.get(
            "/repos/{owner}/{repo}/security-advisories/{ghsa_id}",
            {"ghsa_id": ghsa_id},
            authenticated=True,
        )
        if isinstance(result, dict):
            aliases = []

            if result.get("cve_id"):
                aliases.append(result.get("cve_id"))

            return Advisory(
                ghsa_id=result.get("ghsa_id", ""),
                severity=result.get("severity", "NA"),
                aliases=aliases,
                summary=result.get("summary"),
                cwes=result.get("cwe_ids", []),
            )
        raise Exception(f"Error getting advisory by id")

    def createAdvisory(
        self, advisory: Advisory, repository: Optional[Repository] = None
    ):
        """Create a GitHub Security Advisories for a repository."""
        raise Exception("Unsupported feature")

    def createPrivateAdvisory(
        self, advisory: Advisory, repository: Optional[Repository] = None
    ):
        """Create a GitHub Security Advisories for a repository."""
        raise Exception("Unsupported feature")

    def updateAdvisory(
        self, advisory: Advisory, repository: Optional[Repository] = None
    ):
        """Update GitHub Security Advisory."""
        raise Exception("Unsupported feature")
