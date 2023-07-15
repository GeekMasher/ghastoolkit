from ghastoolkit import Advisories, Advisory
from ghastoolkit.supplychain.dependencies import Dependency


dependency = Dependency.fromPurl("pkg:maven/org.apache.logging/log4j:log4j-core@1.12.0")

advisories = Advisories()
advisories.loadAdvisories(".")

print(f"Advisories :: {len(advisories)}")

log4shell: Advisory = advisories.find("GHSA-jfh8-c2jp-5v3q")

print(f"Advisory({log4shell.ghsa_id}, {log4shell.severity})")

for aff in log4shell.affected:
    print(aff)

print("")
print(f"Dependency :: {dependency.name} ({dependency.version})")
print("Advisories Found:")
for adv in advisories.check(dependency):
    print(f" >>> Advisory({adv.ghsa_id}, `{','.join(adv.aliases)}`)")

