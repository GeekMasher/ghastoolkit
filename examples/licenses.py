"""Licenses using custom data."""
from ghastoolkit import Licenses

# load custom license data
licenses = Licenses()

# load clearlydefined files
licenses.load("../policy-as-code/ghascompliance/data/clearlydefined.json")
licenses.load("../policy-as-code/ghascompliance/data/pyindex5000.json")

print(f" >> {len(licenses)}")

# find dependency
result = licenses.find("com.google.guava/guava")
print(f"License :: {result}")
