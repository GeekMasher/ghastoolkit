import os
import json
from ghastoolkit import DependencyGraph, GitHub
from ghastoolkit.octokit.octokit import GraphQLRequest

GitHub.init(repository=os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))
print(f"Repository :: {GitHub.repository}")

depgraph = DependencyGraph()
dependencies = depgraph.getDependencies()

print(f"Total Dependencies :: {len(dependencies)}")

# or you can get the data from the GraphQL API as well
# This can be useful if you want to get more information about the dependencies
dependencies = depgraph.getDependenciesGraphQL()
print(f"Total Dependencies (GraphQL) :: {len(dependencies)}")

gpl = dependencies.findLicenses(["GPL-*", "AGPL-*"])
print(f"Total GPL Dependencies :: {len(gpl)}")

print("Downloaded SBOM...")
path = "./sbom.spdx"
sbom = depgraph.exportBOM()
with open(path, "w") as handle:
    json.dump(sbom, handle, indent=2)

print(f"Stored SBOM :: {path}")
