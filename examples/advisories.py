from ghastoolkit import Advisories, Advisory, SecurityAdvisories
from ghastoolkit.supplychain.dependencies import Dependency

# SecurityAdvisories REST API helper
security_advisories = SecurityAdvisories()

# get remote security advisories
advisories = security_advisories.getAdvisories()
# load local (json) advisories
advisories.loadAdvisories(".")

print(f"Advisories :: {len(advisories)}")

# get log4shell advisory
log4shell: Advisory = advisories.find("GHSA-jfh8-c2jp-5v3q")

print(f"Advisory({log4shell.ghsa_id}, {log4shell.severity})")


# load Dependency from PURL (log4j vulnerable to log4shell)
dependency = Dependency.fromPurl("pkg:maven/org.apache.logging/log4j:log4j-core@1.12.0")
print(f"Dependency :: {dependency.name} ({dependency.version})")

# display all advisories which affect the dependency
print("Advisories Found:")
for adv in advisories.check(dependency):
    print(f" >>> Advisory({adv.ghsa_id}, `{','.join(adv.aliases)}`)")
