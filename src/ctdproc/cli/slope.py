"""ctdproc slope -- conductivity slope (gain) correction vs bottle/salinometer."""

import sys
import argparse

from ctdproc.slopecorrection_finder import slopecorrection_finder


def build_parser(subparsers=None):
    kwargs = dict(
        help="conductivity slope (gain) correction vs bottle/salinometer",
        description="Fit a per-sensor-pair conductivity slope (gain) correction from CTD "
                    "vs. bottle/salinometer comparisons",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ctdproc slope config_saltcorr.yaml
  ctdproc slope config_saltcorr.yaml --output-dir outputs/
        """,
    )
    if subparsers is not None:
        parser = subparsers.add_parser("slope", **kwargs)
    else:
        parser = argparse.ArgumentParser(prog="ctdproc slope", **kwargs)

    parser.add_argument("config", help="path to a slope-correction-finder YAML config")
    parser.add_argument("--data-dir", "-d", default=None,
                         help="override config's constants.data_dir")
    parser.add_argument("--output-dir", "-o", default=None,
                         help="override config's constants.output_dir")
    return parser


def run(args):
    """Execute the slope subcommand. Returns exit code."""
    try:
        slopecorrection_finder(args.config, data_dir=args.data_dir, output_dir=args.output_dir)
    except Exception as e:
        print(f"Error running slopecorrection_finder: {e}")
        return 1
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
