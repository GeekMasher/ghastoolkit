# Code Scanning API Examples

### Get Code Scanning Alerts

```python
from ghastoolkit import GitHub, CodeScanning
# Initialise GitHub with repository `owner/name`
GitHub.init("GeekMasher/ghastoolkit")

# Initialise a CodeScanning instance
cs = CodeScanning()

# Get all the open alerts
alerts = cs.getAlerts("open")

print(f"Alerts :: {alerts}")
```
