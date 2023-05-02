
from ghastoolkit import GitHub, SecretScanning

GitHub.init("octodemo/demo-ghas-geekmasher")

# Setup Secret Scanning
secret_scanning = SecretScanning()
alerts = secret_scanning.getAlerts("open")

print(f"Alert Count :: {len(alerts)}")

# Single Secret
alert = secret_scanning.getAlert(4)
print(alert)


# locations
for loc in alert.locations:
    print(f" >> {loc}")


