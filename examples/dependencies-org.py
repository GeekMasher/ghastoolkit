"""Example fetching all of the dependencies for an organization.

This example also caches the results to a local folder.
"""

import os
import logging
from ghastoolkit import GitHub, DependencyGraph
from ghastoolkit.utils.cache import Cache, CACHE_WEEK

# Set the logging for ghastoolkit
ghastoolkit_logger = logging.getLogger("ghastoolkit")
ghastoolkit_logger.setLevel(logging.DEBUG)
# Set the cache to be for a week
Cache.cache_age = CACHE_WEEK

# Initialize GitHub with the token
GitHub.init("GeekMasherOrg", token=os.environ.get("GITHUB_TOKEN"))

print(f"GitHub :: {GitHub}")
print(f"Owner  :: {GitHub.owner}")
print(f"Token  :: {GitHub.getToken()} ({GitHub.token_type})")

depgraph = DependencyGraph(cache=True)
print(f"Cache  :: {depgraph.cache.cache_path}")

# OR Get the list of unique dependencies
unique = depgraph.getUniqueOrgDependencies(version=False)

print(f"Unique dependencies: {len(unique)}")
print("\nDependencies:")
for dep in unique:
    # Example filter for a specific dependency
    if dep.fullname == "github/codeql-action/analyze":
        if len(dep.repositories) == 0:
            continue

        # Every dependencies has a list of repositories that use it
        print(f"{dep}")
        for r in dep.repositories:
            print(f"\t> {r}")
