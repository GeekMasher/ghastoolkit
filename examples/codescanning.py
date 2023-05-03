
from ghastoolkit import GitHub, CodeScanning

GitHub.init("GeekMasher/ghastoolkit")

cs = CodeScanning()

# Get all alerts
alerts = cs.getAlerts("open")
print(f"Alert Count :: {len(alerts)}")


if GitHub.repository.isInPullRequest():
    # Get list of the delta alerts in a PR
    delta = cs.getAlertsInPR("refs/heads/master")
    print(f"Delta :: {len(delta)}")

