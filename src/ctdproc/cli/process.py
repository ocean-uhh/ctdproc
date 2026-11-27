"""ctdproc process -- full per-cast CTD processing pipeline."""

import sys
import argparse

from ctdproc.main import CTD_process


def build_parser(subparsers=None):
    kwargs = dict(
        help="full per-cast CTD processing pipeline",
        description="Run the full per-cast CTD processing pipeline from a YAML config",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ctdproc process config.yaml
  ctdproc process config.yaml --data-dir ../data --output-dir outputs/
        """,
    )
    if subparsers is not None:
        parser = subparsers.add_parser("process", **kwargs)
    else:
        parser = argparse.ArgumentParser(prog="ctdproc process", **kwargs)

    parser.add_argument("config", help="path to a cast-processing YAML config")
    parser.add_argument("--data-dir", "-d", default=None,
                         help="override config's constants.data_dir")
    parser.add_argument("--output-dir", "-o", default=None,
                         help="override config's constants.output_dir")
    return parser


def run(args):
    """Execute the process subcommand. Returns exit code."""
    try:
        CTD_process(args.config, data_dir=args.data_dir, output_dir=args.output_dir)
    except Exception as e:
        print(f"Error running CTD_process: {e}")
        return 1
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
