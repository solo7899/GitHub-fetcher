import argparse
import sqlite3



def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch and process Git repositories.")
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="The URL of the Git repository to fetch.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="The directory where the fetched repository will be stored (default: ./output).",
    )
    return parser.parse_args()


def connect_to_database():   
    conn = sqlite3.connect('repositories.db')
    cursor = conn.cursor()
    return conn, cursor


if __name__ == "__main__":
    args = parse_arguments()
    if not args.repo:
        print("Error: --repo argument is required.")
        exit(1)
    print(f"Repository URL: {args.repo}")

    conn, cursor = connect_to_database()