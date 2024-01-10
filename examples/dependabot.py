"""Dependabot API example."""
import os
from ghastoolkit import Dependabot, GitHub

GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"),
)

dependabot = Dependabot()

if not dependabot.isEnabled():
    print("Dependabot is not enabled")
    exit(1)

alerts = dependabot.getAlerts()
print(f"Total Alerts :: {len(alerts)}")

for alert in alerts:
    print(f"Alert :: {alert}")
