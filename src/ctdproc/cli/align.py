"""ctdproc align -- lead/lag time offset via cross-correlation."""

import sys
import argparse

from ctdproc.ctdalign_finder import ctdalign_finder


def build_parser(subparsers=None):
    kwargs = dict(
        help="lead/lag time offset via cross-correlation",
        description="Measure the time lag between a lead/lag variable pair across a range "
                    "of casts, via cross-correlation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Config: needs an 'alignment_settings' block, one entry per lead/lag pair to
check:
  alignment_settings:
    variable_lead: [...]      # the leading variable, e.g. pressure
    variable_lag: [...]       # the lagging variable to align, e.g. conductivity
    max_lag: [...]            # max lag to search, in scans
    pressure_upper: [...]     # upper pressure bound for the search window (dbar)
    pressure_lower: [...]     # lower pressure bound for the search window (dbar)
All five lists must be the same length - one entry per pair.

Output: alignment_report.csv (per-cast + campaign-average lag, in a sign
already matching the 'align' feature step's own offset: convention).

Examples:
  ctdproc align config_align.yaml
  ctdproc align config_align.yaml --output-dir outputs/
        """,
    )
    if subparsers is not None:
        parser = subparsers.add_parser("align", **kwargs)
    else:
        parser = argparse.ArgumentParser(prog="ctdproc align", **kwargs)

    parser.add_argument("config", help="path to an alignment-finder YAML config")
    parser.add_argument("--data-dir", "-d", default=None,
                         help="override config's constants.data_dir")
    parser.add_argument("--output-dir", "-o", default=None,
                         help="override config's constants.output_dir")
    return parser


def run(args):
    """Execute the align subcommand. Returns exit code."""
    try:
        ctdalign_finder(args.config, data_dir=args.data_dir, output_dir=args.output_dir)
    except Exception as e:
        print(f"Error running ctdalign_finder: {e}")
        return 1
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
