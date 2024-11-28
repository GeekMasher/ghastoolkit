import logging
from dataclasses import dataclass, field
from typing import Dict, Optional, List

from ghastoolkit.errors import GHASToolkitError
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.octokit import RestRequest, OctoItem, loadOctoItem
from ghastoolkit.octokit.enterprise import Organization


logger = logging.getLogger("ghastoolkit.octokit.github")

@dataclass
class BillingResponse(OctoItem):
    """Billing Response."""

    total_advanced_security_committers: int
    """Total Advanced Security Committers."""
    total_count: int
    """Total Count."""
    maximum_advanced_security_committers: int
    """Maximum Advanced Security Committers."""
    purchased_advanced_security_committers: int
    """Purchased Advanced Security Committers."""

    repositories: List[Dict] = field(default_factory=list)
    """Repositories."""

    @property
    def active(self) -> int:
        """Active Advanced Security Committers."""
        return self.total_advanced_security_committers
    
    @property
    def maximum(self) -> int:
        """Maximum Advanced Security Committers."""
        return self.maximum_advanced_security_committers
    
    @property
    def purchased(self) -> int:
        """Purchased Advanced Security Committers."""
        return self.purchased_advanced_security_committers


@dataclass
class BillingRepository(OctoItem):
    """Billing Repository."""
    name: str
    """Repository Name."""
    advanced_security_committers: int
    """Advanced Security Committers."""
    advanced_security_committers_breakdown: Dict = field(default_factory=dict) 
    """Advanced Security Committers Breakdown."""

    def activeCommitterNames(self) -> List[str]:
        """Active Committer Names."""
        results = []
        for commiter in self.advanced_security_committers_breakdown:
            results.append(commiter.get("user_login"))
        return results

    def activeCommitterEmails(self) -> List[str]:
        """Active Committer Emails."""
        results = []
        for commiter in self.advanced_security_committers_breakdown:
            results.append(commiter.get("last_pushed_email"))
        return results


class Billing:
    """GitHub Billing API"""

    def __init__(self, organization: Optional[Organization] = None) -> None:
        """Initialise Billing API."""
        self.org = organization.name or GitHub.owner
        self.rest = RestRequest()
        self.state = None

    def getGhasBilling(self) -> BillingResponse:
        """Get GitHub Advanced Security Billing."""
        result = self.rest.get(f"/orgs/{self.org}/settings/billing/advanced-security")

        if isinstance(result, dict):
            return loadOctoItem(BillingResponse, result)

        logger.error("Error getting billing")
        raise GHASToolkitError(
            "Error getting billing",
            permissions=["Enterprise billing permissions (read:actions)"],
            docs="https://docs.github.com/en/rest/reference/billing",
        )

    def loadFromCsv(self) -> BillingResponse:
        """Load Billing from CSV."""
        pass
