import logging
from typing import List, Optional

from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.octokit import Octokit, RestRequest
from ghastoolkit.octokit.repository import Repository

logger = logging.getLogger("ghastoolkit.octokit.enterprise")


class Organization:
    """Organization."""

    def __init__(
        self, organization: Optional[str] = None, identifier: Optional[int] = None
    ) -> None:
        """Initialise Organization."""
        self.name = organization
        self.id = identifier

        self.rest = RestRequest(GitHub.repository)

    def getRepositories(self) -> List[Repository]:
        """Get Repositories."""
        repositories = []
        result = self.rest.get(f"/orgs/{self.name}/repos")
        if not isinstance(result, list):
            logger.error("Error getting repositories")
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
        """Get all the Organizations in an enterprise.

        You will need to be authenticated as an enterprise owner to use this API.
        """
        organizations = []
        url = Octokit.route("/organizations", GitHub.repository)
        # pagination uses a different API versus the rest of the API
        # https://docs.github.com/en/enterprise-cloud@latest/rest/orgs/orgs#list-organizations
        last_org_id = 1

        while True:
            response = self.rest.session.get(
                url, params={"since": last_org_id, "per_page": 100}
            )

            if response.status_code != 200:
                logger.error("Error getting organizations")
                return []

            result = response.json()

            if not isinstance(result, list):
                logger.error("Error getting organizations")
                return []

            for org in result:
                organizations.append(Organization(org.get("login"), org.get("id")))

            if len(result) < 100:
                break
            # set last org ID
            last_org_id = organizations[-1].id

        return organizations