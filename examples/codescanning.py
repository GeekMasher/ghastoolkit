"""Example showing how to connect and use the Code Scanning API.
"""

import os
from ghastoolkit import GitHub, CodeScanning

GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"),
    reference=os.environ.get("GITHUB_REF", "refs/heads/main"),
)

cs = CodeScanning()

print(f"Repository :: {GitHub.repository}")

# requires "Repository Administration" repository permissions (read)
if not cs.isEnabled():
    print("Code Scanning is not enabled :(")
    exit()

# Get list of the delta alerts in a PR
if GitHub.repository.isInPullRequest():
    alerts = cs.getAlertsInPR("refs/heads/main")

# Get all alerts
else:
    alerts = cs.getAlerts("open")

print(f"Alert Count :: {len(alerts)}")

for alert in alerts:
    print(f" >> {alert} ({alert.severity})")

# get latest analyses for each tool
analyses = cs.getLatestAnalyses()
print(f"Analyses :: {len(analyses)}")

# get list of tools
tools = cs.getTools()
print(f"Tools :: {tools}")
