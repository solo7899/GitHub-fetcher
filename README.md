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
- `--output` or `-o`: Output listed repositories to a JSON file (`<owner>.json`)
- `--refresh` or `-r`: Refresh (delete and re-fetch) repositories for the owner
- `--verbose` or `-v`: Enable verbose output

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

## Database

- The script creates a local SQLite database file named `repositories.db` in the project directory.
- Table: `repositories` (id, owner, name, language, html_url)

---

_Created ️ by SOLO7899_
