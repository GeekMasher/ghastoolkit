"""Dependabot API example."""
import os
from ghastoolkit import Dependabot, GitHub

GitHub.init(os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))

depgraph = Dependabot()

alerts = depgraph.getAlerts()
print(f"Total Alerts :: {len(alerts)}")
