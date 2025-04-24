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

# GraphQL is required to get the full dependencies details
depgraph = DependencyGraph(cache=True, enable_graphql=True)
print(f"Cache  :: {depgraph.cache.cache_path}")

# Get the list of unique dependencies (ignoring versions)
unique = depgraph.getUniqueOrgDependencies(version=False)

print(f"Unique dependencies: {len(unique)}")

direct = unique.findDirectDependencies()
print(f"Direct dependencies: {len(direct)}\n")

for dep in direct:
    # Every dependencies has a list of repositories that use it
    print(f"{dep}")
    for r in dep.repositories:
        print(f"\t> {r}")
