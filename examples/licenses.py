"""Licenses using custom data."""
from ghastoolkit import Licenses

# load custom license data
licenses = Licenses()
print(f" >> {len(licenses)}")

# find dependency
result = licenses.find("com.google.guava/guava")
print(f"License :: {result}")
