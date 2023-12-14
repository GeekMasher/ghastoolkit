"""Dependabot API example."""
import os
from ghastoolkit import Dependabot, GitHub

GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"),
    # using a PAT
    token=os.environ.get("GHASTOOLKIT_PAT"),
)

depgraph = Dependabot()

alerts = depgraph.getAlerts()
print(f"Total Alerts :: {len(alerts)}")

for alert in alerts:
    print(f"Alert :: {alert}")
