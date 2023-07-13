
import os
from ghastoolkit import GitHub, CodeScanning

GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"),
)
print(f" >> {GitHub.repository}")

cs = CodeScanning()

alerts = cs.getAlerts("open", ref=GitHub.repository.reference)

# Get list of the delta alerts in a PR
if GitHub.repository.isInPullRequest():
    delta = cs.getAlertsInPR("refs/heads/main")
    print(f"Delta :: {len(delta)}")

# Get all alerts
else:
    alerts = cs.getAlerts("open")
    print(f"Alert Count :: {len(alerts)}")

# get latest analyses for each tool 
analyses = cs.getLatestAnalyses()
print(f"Analyses :: {len(analyses)}")

# get list of tools
tools = cs.getTools()
print(f"Tools :: {tools}")

