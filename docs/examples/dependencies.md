# Dependency Graph

## Organization

To get a list of all the dependencies in an organization, your'll need to setup `DependencyGraph`.

```python
from ghastoolkit import GitHub, DependencyGraph

GitHub.init("GeekMasher/ghastoolkit")
print(f"Owner :: {GitHub.repository.owner}")
```

After that, we can use the graph to pull a dict of repositories and associated dependencies:

```python
depgraph = DependencyGraph()

dependencies = depgraph.getOrganizationDependencies()

for repo, deps in dependencies.items():
    print(f" > {repo.display} :: {len(deps)}")
```

Once you have this information, you can look up dependencies usages across the
organization or get other data from it.

## Snapshots

To upload a snapshot to the Dependency Graph you can use the `DependencyGraph` octokit API.

Lets start by importing and setting up `GitHub`.

```python
import json
from ghastoolkit import DependencyGraph, Dependencies

# initialise GitHub
GitHub.init("GeekMasher/ghastoolkit")

# create DependencyGraph API
depgraph = DependencyGraph()
```

Once you have a DependencyGraph ready, you with need to create a list of `Dependencies`.

```python
dependencies = Dependencies()
# ... create list of dependencies

```

Once you have the list, you can simply call the following API:

```python
depgraph.submitDependencies(dependencies)
```

This function converts the list of dependencies to a SPDX and submits the data to the Dependency Graph API.
