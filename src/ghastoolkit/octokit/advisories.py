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
        return Advisories()

    def getAdvisory(self, ghsa_id: str) -> Optional[Advisory]:
        """Get advisory by ghsa id."""
        return

    def createAdvisory(
        self, advisory: Advisory, repository: Optional[Repository] = None
    ):
        """Create a GitHub Security Advisories for a repository."""
        return

    def createPrivateAdvisory(
        self, advisory: Advisory, repository: Optional[Repository] = None
    ):
        """Create a GitHub Security Advisories for a repository."""
        return

    def updateAdvisory(
        self, advisory: Advisory, repository: Optional[Repository] = None
    ):
        """Update GitHub Security Advisory."""
        return
