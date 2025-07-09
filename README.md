# Git Repos Fetcher

A Python command-line tool to fetch, store, list, and manage public GitHub repositories for a specified user. Repository data is stored in a local SQLite database for easy querying and management.

## Features

- Fetches all public repositories for a given GitHub user
- Stores repository info (owner, name, language, URL) in a local SQLite database
- Lists repositories for a user from the database
- Outputs repository data to a JSON file
- Optionally refreshes (updates) the database for a user
- Verbose mode for detailed output

## Requirements

- Python 3.7+
- `requests` library

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line:

```bash
python git_fetcher.py --owner <github_username> [options]
```

### Options

- `--owner <username>` (required): GitHub username to fetch repositories for
- `--list` or `-l`: List repositories for the owner from the database
- `--output` or `-o`: Output listed or fetched repositories to a JSON file (`<owner>.json`)
- `--refresh` or `-r`: Refresh (delete and re-fetch) repositories for the owner
- `--verbose` or `-v`: Enable verbose output

### Behavior

- If `--list` is used, repositories are listed from the database. If `--output` is also used, the list is saved to `<owner>.json`.
- If `--refresh` is used, existing repositories for the owner are deleted from the database before fetching new data.
- If the owner already exists in the database and `--refresh` is not used, the script will exit with a message.
- If `--output` is used without `--list`, fetched repositories are saved to `<owner>.json` after fetching from GitHub.

### Examples

Fetch and store repositories for a user:

```bash
python git_fetcher.py --owner octocat
```

List repositories for a user:

```bash
python git_fetcher.py --owner octocat --list
```

List and output to JSON:

```bash
python git_fetcher.py --owner octocat --list --output
```

Refresh repositories for a user:

```bash
python git_fetcher.py --owner octocat --refresh
```

Fetch and output to JSON:

```bash
python git_fetcher.py --owner octocat --output
```

## Database

- The script creates a local SQLite database file named `repositories.db` in the project directory.
- Table: `repositories` (id, owner, name, language, html_url)
- The `html_url` field is unique to prevent duplicate entries.

## Output

- JSON output files are named `<owner>.json` and contain either the fetched or listed repositories.
- The JSON structure is a list of objects with keys: `owner`, `name`, `language`, `html_url`.

---

_Created by SOLO7899_
