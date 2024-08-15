"""Dependabot API example."""
import os
from ghastoolkit import Dependabot, GitHub

GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"),
    reference=os.environ.get("GITHUB_REF", "refs/heads/main"),
)

dependabot = Dependabot()

if not dependabot.isEnabled():
    print("Dependabot is not enabled")
    exit(1)

if GitHub.repository.isInPullRequest():
    print("Dependabot Alerts from Pull Request")
    alerts = dependabot.getAlertsInPR()
else:
    print("Dependabot Alerts from Repository")
    alerts = dependabot.getAlerts()

print(f"Total Alerts :: {len(alerts)}")

for alert in alerts:
    print(f"Alert :: {alert}")
