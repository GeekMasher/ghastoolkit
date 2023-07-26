"""CodeQL Packs examples."""
import logging
from ghastoolkit import CodeQLPack

logging.basicConfig(level=logging.DEBUG)

# download
pack = CodeQLPack.download("codeql/python-queries", "0.7.4")
print(f"Remote Pack :: {pack}")
# local loading
pack = CodeQLPack("./examples/packs")
print(f"Local Pack  :: {pack}")

# install dependencies
pack.install(True)

path = pack.create()
print(f"Pack Path :: {path}")

queries = pack.resolveQueries()
print("")
print(f"# Queries :: {len(queries)}")
for query in queries:
    print(f" - {query}")
