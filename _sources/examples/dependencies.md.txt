# Dependency Graph

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
