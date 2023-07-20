"""Secret Scanning API example."""
import os
from ghastoolkit import GitHub, SecretScanning

GitHub.init(os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))

# Setup Secret Scanning
secret_scanning = SecretScanning()
alerts = secret_scanning.getAlerts("open")

print(f"Alert Count :: {len(alerts)}")

# Single Secret
alert = secret_scanning.getAlert(4)
print(f"Secret :: {alert}")

# locations
for loc in alert.locations:
    print(f" >> {loc}")
