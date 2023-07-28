"""Secret Scanning API example."""
import os
from ghastoolkit import GitHub, SecretScanning

GitHub.init(os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))

# Setup Secret Scanning
secret_scanning = SecretScanning()

if not secret_scanning.isEnabled():
    print("Secret Scanning is disabled :(")
    exit(1)

print(f"Push Protection :: {secret_scanning.isPushProtectionEnabled()}")

try:
    alerts = secret_scanning.getAlerts("open")
except:
    print("[!] Error getting alerts, check access")
    exit(0)

print(f"Alert Count :: {len(alerts)}")

# Display Secrets
for alert in alerts:
    print(f"- Secret :: {alert}")
    # locations
    for loc in alert.locations:
        print(f" >> {loc}")

print("Finished!")
