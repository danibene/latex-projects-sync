# Latex Projects Sync

This project is designed to facilitate the synchronization of LaTeX projects across multiple GitHub repositories, which can be in turn synchronized with Overleaf.

It specifically focuses on syncing .bib (BibTeX) and .tex (LaTeX) files, identifying segments marked for synchronization within these files and ensures they are consistent across different repositories. I personally used it for updating my thesis while working on an article that was included as a chapter at the same time.

## Features

- Supports `.bib` and `.tex` files for synchronization.
- Allows specifying sync direction (`TO` or `FROM`) to control sync flow.
- Uses GitHub tokens for authentication.
- Automates the tedious process of manually ensuring consistency across multiple LaTeX projects.

## Prerequisites

- `github` Python package for interacting with the GitHub API
- `json_tricks` Python package for handling JSON operations

## Setup

1. **Install Required Python Packages:**

    ```bash
    pip install PyGithub json-tricks
    ```

2. **Configuration:**

    Create a `local_secrets` directory at the root of your project and add a `secrets.json` file with the following structure:

    ```json
    {
      "ACCESS_TOKEN_GITHUB": "your_github_access_token",
      "REPO_PATHS_GITHUB": "user/repo1, user/repo2"
    }
    ```

    Alternatively, you can set `ACCESS_TOKEN_GITHUB` and `REPO_PATHS_GITHUB` as environment variables.

3. **Authentication:**

    The script uses a GitHub access token for authentication. Ensure your token has the necessary permissions to read from and write to the specified repositories.

## Usage

To run the synchronization process, simply execute the script:

```bash
python latex_projects_sync.py
```

The script will automatically find and synchronize the marked segments in your `.bib` and `.tex` files across the specified repositories.

## Marking Content for Synchronization

To mark content for synchronization, enclose it within the following markers in your `.bib` or `.tex` files:

```latex
%%%START_SYNC_TO_label%
Content to sync
%%%STOP_SYNC_TO_label%

%%%START_SYNC_FROM_label%
Content to sync
%%%STOP_SYNC_FROM_label%
```

Replace `label` with a unique identifier for the content block. Ensure that the start and stop markers use the same label.
