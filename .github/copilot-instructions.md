# F3RVA Content Migration - Copilot Instructions

This document provides instructions for AI coding agents to effectively contribute to the `f3rva-content-migration` project.

## Project Overview

This is a Python command-line interface (CLI) tool built with `click` to migrate content from WordPress APIs into a structured database. The core functionality involves calling various standard and custom WordPress APIs, extracting specific fields for each post, and then calling a database update function.

## Core Architecture

The application is structured around the `click` CLI framework, with a central dispatcher and modular, subcommand-based scripts.

- **Main Entry Point (`src/f3rva_content_migration/cli.py`):** This file defines the main `click.group()` and acts as a router, aggregating commands from other modules. It does not contain business logic itself.

- **Command Scripts (`src/f3rva_content_migration/scripts/`):** Each file in this directory implements a specific CLI command as a `@click.command()`.
  - **`hello_world.py`:** A simple command for testing the CLI setup.

- **Project Configuration (`pyproject.toml`):** This file manages project dependencies and defines the script entry points. The `[project.scripts]` section maps commands like `f3rva-migrate` to the `cli:main` function.

## Developer Workflow

### 1. Setup

To work on this project, you must install it in "editable" mode. This makes the CLI commands available in your shell's path.

```bash
# Install the project and its dependencies
pip install -e .
```

### 2. Running Commands

Once installed, you can run commands directly from the terminal. The main command group is `f3rva-migrate`.

```bash
# Run the hello world test script
f3rva-migrate hello
```

### 3. Adding a New Command

To add a new command (e.g., `new-command`):

1.  Create a new file: `src/f3rva_content_migration/scripts/new_command.py`.
2.  In that file, define a function using the `@click.command()` decorator.
3.  Import your new command function in `src/f3rva_content_migration/cli.py`.
4.  Register it with the main group: `main.add_command(new_command)`.

## Key Conventions

- **CLI with Click:** All CLI functionality is built using the `click` library. New commands should follow this pattern, using decorators for arguments and options.
- **Database Abstraction:** The database logic is intentionally separated into the `update_database_record` function. This function is a placeholder and should be implemented with the appropriate database connector library (e.g., `sqlite3`, `psycopg2`).
- **Dependency Management:** Core dependencies are listed in `pyproject.toml`. Do not use `requirements.txt` for adding new dependencies.
