import argparse
import sqlite3
import requests


def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch and process Git repositories.")
    parser.add_argument(
        "--owner",
        type=str,
        required=True,
        help="The owner of the Git acount to fetch.",
    )
    parser.add_argument(
        "--output",
        action="store_true",
        help="If set, output the fetched repository content to a file.",
    )
    return parser.parse_args()

def output_json(api_output, filename):
    with open(f"{filename}.json", "w") as file:
        file.write(api_output)

def connect_to_database():   
    conn = sqlite3.connect('repositories.db')
    cursor = conn.cursor()
    return conn, cursor

def request_repository(username):
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching repository: {e}")
        return None

if __name__ == "__main__":
    args = parse_arguments()
    if not args.owner:
        print("Error: --owner argument is required.")
        exit(1)
    print(f"Git owner: {args.owner}")

    conn, cursor = connect_to_database()

    repo_content = request_repository(args.owner)
    if repo_content is None:
        print("Failed to fetch repository content.")
        exit(1)
    print(f"Fetched content from {args.owner}")

    if args.output:
        output_json(repo_content, args.owner)