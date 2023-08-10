import os
import logging
import argparse
from ghastoolkit.codeql.cli import CodeQL

parser = argparse.ArgumentParser("ghastoolkit-codeql")
parser.add_argument("--debug", action="store_true")

parser_codeql = parser.add_argument_group("codeql")
parser.add_argument("mode", choices=["", "init", "analyze", "update"])
parser_codeql.add_argument("-b", "--binary")
parser_codeql.add_argument("-c", "--command", type=str)


arguments = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG if arguments.debug or os.environ.get("DEBUG") else logging.INFO,
    format="%(message)s",
)

codeql = CodeQL()

if not codeql.exists():
    logging.error(f"Failed to find codeql on system")
    exit(1)

# if arguments.mode in ["", ""]

logging.info(f"Finished!")
