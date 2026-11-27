"""ctdproc command-line interface.

Entry point: the `ctdproc` command dispatches to subcommands.

  ctdproc process  -- full per-cast CTD processing pipeline
  ctdproc slope    -- conductivity slope (gain) correction vs bottle/salinometer
  ctdproc align    -- lead/lag time offset via cross-correlation
  ctdproc celltm   -- cell thermal mass (alpha, tau) grid search
"""

import sys
import argparse

from ctdproc.cli import process as _process
from ctdproc.cli import slope as _slope
from ctdproc.cli import align as _align
from ctdproc.cli import celltm as _celltm


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ctdproc",
        description="CTD processing",
    )
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="COMMAND")
    subparsers.required = True

    _process.build_parser(subparsers)
    _slope.build_parser(subparsers)
    _align.build_parser(subparsers)
    _celltm.build_parser(subparsers)

    args = parser.parse_args(argv)

    if args.command == "process":
        return _process.run(args)
    if args.command == "slope":
        return _slope.run(args)
    if args.command == "align":
        return _align.run(args)
    if args.command == "celltm":
        return _celltm.run(args)


if __name__ == "__main__":
    sys.exit(main())
