from typing import List, Optional

from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.octokit import RestRequest
from ghastoolkit.octokit.repository import Repository


class Organization:
    """Organization."""

    def __init__(self, organization: Optional[str] = None) -> None:
        """Initialise Organization."""
        self.name = organization
        self.rest = RestRequest(GitHub.repository)

    def getRepositories(self) -> List[Repository]:
        """Get Repositories."""
        repositories = []
        result = self.rest.get("/orgs/{org}/repos", params={"org": self.name})
        if not isinstance(result, list):
            print("Error getting repositories")
            return []

        for repository in result:
            repositories.append(repository.parseRepository(repository.get("full_name")))

        return repositories


class Enterprise:
    """Enterprise API."""

    def __init__(
        self,
        enterprise: Optional[str] = None,
    ) -> None:
        """Initialise Enterprise."""
        self.enterprise = enterprise or GitHub.enterprise
        self.rest = RestRequest(GitHub.repository)

    def getOrganizations(self) -> List[Organization]:
        """Get Organizations."""
        organizations = []
        result = self.rest.get("/organizations")
        if not isinstance(result, list):
            print("Error getting organizations")
            return []
        for org in result:
            organizations.append(Organization(org.get("login")))
        return organizations
