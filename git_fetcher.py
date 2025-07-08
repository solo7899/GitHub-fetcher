import argparse
import sqlite3
import requests
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch and process Git repositories.")
    parser.add_argument(
        "--owner",
        type=str,
        required=True,
        help="The owner of the Git acount to fetch.",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List the specified owner repos from db",
    )
    parser.add_argument(
        "--output", "-o",
        action="store_true",
        help="If set, output the fetched repository content to a file.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="makes  verbose"
    )
    return parser.parse_args()

def output_json(api_output, filename):
    with open(f"{filename}.json", "w") as file:
        file.write(api_output)

def connect_to_database():   
    conn = sqlite3.connect('repositories.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS repositories (
            id INTEGER PRIMARY KEY,
            owner TEXT,
            name TEXT,
            language TEXT, 
            html_url TEXT UNIQUE
        )''')
    return conn, cursor

def request_repository(username, verbose):
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        if verbose:
            print(f"Error fetching repository: {e}")
        return None

def json_parser(json_input, verbose):
    repos = []
    try:
        data = json.loads(json_input)
        for repo in data:
            if verbose:
                print(f"Repository Name: {repo['name']}, Language: {repo['language']}, URL: {repo['html_url']}")
            repos.append({
                "owner": repo.get("owner", {}).get("login"),
                "name": repo.get("name"),
                "language": repo.get("language"),
                "html_url": repo.get("html_url"),
            }) 
        return repos
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}") 
        return []

def save_to_db(cursor, parsed_data):
    for data in parsed_data:
        try:
            cursor.execute('''
                INSERT INTO repositories (owner, name, language, html_url)
                VALUES (?, ?, ?, ?)
            ''', (data['owner'], data['name'], data['language'], data['html_url']))
        except sqlite3.Error as e:
            print(f"Error: {e}")

def list_repos(owner, cursor:sqlite3.Cursor):
    cursor.execute('''
        SELECT * FROM repositories WHERE owner ==  ?
    ''', (owner,))
    return cursor.fetchall()

if __name__ == "__main__":
    args = parse_arguments()
    if not args.owner:
        print("Error: --owner argument is required.")
        exit(1)
    if args.verbose:
        print(f"Git owner: {args.owner}")

    conn, cursor = connect_to_database()

    if args.list:
        repos = list_repos(args.owner, cursor)
        for repo in repos:
            print(repo)

        if args.output:
            output_json(repos, args.owner)

        cursor.close()
        conn.close()
        exit(0)

    repo_content = request_repository(args.owner, args.verbose)
    if repo_content is None:
        print("Failed to fetch repository content.")
        exit(1)
    if args.verbose:
        print(f"Fetched content from {args.owner}")

    json_data_parsed = json_parser(repo_content)
    save_to_db(cursor, json_data_parsed)

    conn.commit()
    cursor.close()
    conn.close()