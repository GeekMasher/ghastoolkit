import json
from ghastoolkit.octokit.dependencygraph import DependencyGraph
from ghastoolkit.octokit.github import GitHub

GitHub.init("GeekMasher/ghastoolkit")

depgraph = DependencyGraph()
dependencies = depgraph.getDependencies()

print(f"Total Dependencies :: {len(dependencies)}")

gpl = dependencies.findLicenses(["GPL-*", "AGPL-*"])
print(f"Total GPL Dependencies :: {len(gpl)}")

print("Downloaded SBOM...")
path = "./sbom.spdx"
sbom = depgraph.exportBOM()
with open(path, "w") as handle:
    json.dump(sbom, handle, indent=2)

print(f"Stored SBOM :: {path}")
