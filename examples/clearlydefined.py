
from ghastoolkit.octokit.clearlydefined import ClearlyDefined
from ghastoolkit.supplychain.dependencies import Dependency

dependency = Dependency("requests", manager="pypi")

clearly = ClearlyDefined()

licenses = clearly.getLicenses(dependency)
print(licenses)

