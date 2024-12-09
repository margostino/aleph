import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Aleph")
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Query to search for",
    )
    return parser.parse_args()
