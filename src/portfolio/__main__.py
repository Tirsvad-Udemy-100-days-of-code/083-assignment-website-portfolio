"""!
@file __main__.py
@brief Entry point of `python -m portfolio`.
"""

import argparse
from collections.abc import Sequence

from portfolio.constants import APP_DESCRIPTION, APP_NAME


def build_parser() -> argparse.ArgumentParser:
    """!
    @brief Create the command line parser.
    @return The parser of the program.
    """
    return argparse.ArgumentParser(
        prog=f"python -m {APP_NAME}",
        description=APP_DESCRIPTION,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """!
    @brief Run the program.
    @param argv The command line arguments; `sys.argv` when None.
    @return The process exit code.
    """
    build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
