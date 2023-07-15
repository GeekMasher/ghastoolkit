# Custom Advisories

First lets import and load our dependency (in our test case, `log4j-core`)

```python
from ghastoolkit import Advisories, Advisory, Dependency

# Load Dependency from PURL
dependency = Dependency.fromPurl(
    "pkg:maven/org.apache.logging/log4j:log4j-core@1.12.0"
)
```

Then we want to create and load our advisories (in our case, `log4shell` / `CVE-2021-44228`)

```python
# create a new list of Advisories
advisories = Advisories()
# load advisories from path
advisories.loadAdvisories(".")

print(f"Advisories :: {len(advisories)}")
```

Lets now just find and display the advisory to make sure its loaded.

```python
# find an advisories by GHSA ID ('CVE-2021-44228' would be the same)
log4shell: Advisory = advisories.find("GHSA-jfh8-c2jp-5v3q")

print(f"Advisory({log4shell.ghsa_id}, {log4shell.severity})")
```

Finally, lets check to see if the dependency has a known advisories associated with it.

```python
print(f"Dependency :: {dependency.name} ({dependency.version})")

# check in the advisories list if dependency is affected
print("Advisories Found::")
for adv in advisories.check(dependency):
    # display GHSA ID and aliases
    print(f" >>> Advisory({adv.ghsa_id}, `{','.join(adv.aliases)}`)")

```

In our case, it shows the following:

```log
Dependency :: log4j:log4j-core (1.12.0)
Advisories Found:
 >>> Advisory(GHSA-jfh8-c2jp-5v3q, `CVE-2021-44228`)
```

See all [examples here](https://github.com/GeekMasher/ghastoolkit/tree/main/examples)

