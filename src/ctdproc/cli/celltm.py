"""ctdproc celltm -- cell thermal mass (alpha, tau) grid search."""

import sys
import argparse

from ctdproc.cellTM_finder import cellTM_finder


def build_parser(subparsers=None):
    kwargs = dict(
        help="cell thermal mass (alpha, tau) grid search",
        description="Grid-search the cell thermal mass (alpha, tau) correction that "
                    "minimizes the down/up-cast salinity difference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ctdproc celltm config_celltm.yaml
  ctdproc celltm config_celltm.yaml --output-dir outputs/
        """,
    )
    if subparsers is not None:
        parser = subparsers.add_parser("celltm", **kwargs)
    else:
        parser = argparse.ArgumentParser(prog="ctdproc celltm", **kwargs)

    parser.add_argument("config", help="path to a celltm-finder YAML config")
    parser.add_argument("--data-dir", "-d", default=None,
                         help="override config's constants.data_dir")
    parser.add_argument("--output-dir", "-o", default=None,
                         help="override config's constants.output_dir")
    return parser


def run(args):
    """Execute the celltm subcommand. Returns exit code."""
    try:
        cellTM_finder(args.config, data_dir=args.data_dir, output_dir=args.output_dir)
    except Exception as e:
        print(f"Error running cellTM_finder: {e}")
        return 1
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
