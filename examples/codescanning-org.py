"""Example showing how to connect and use the Code Scanning for an organization.
"""

import os
from ghastoolkit import GitHub, CodeScanning

GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasherOrg"),
    reference=os.environ.get("GITHUB_REF", "refs/heads/main"),
)

cs = CodeScanning()

print(f"Fetching alerts for {GitHub.owner}...")
alerts = cs.getOrganizationAlerts("open")

print(f"Alerts :: {len(alerts)}")
