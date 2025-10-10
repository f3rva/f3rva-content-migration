"""
Command Line Interface for F3RVA Content Migration

This module provides the main CLI entry point for the content migration tools.
"""

import sys
import argparse
from typing import List, Optional


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="f3rva-migrate",
        description="F3RVA Content Migration Tools",
        epilog="For more information, visit: https://github.com/f3rva/f3rva-content-migration"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )
    
    # Hello command for testing
    hello_parser = subparsers.add_parser(
        "hello",
        help="Say hello (test command)"
    )
    hello_parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)"
    )
    
    # Placeholder for future migration commands
    migrate_parser = subparsers.add_parser(
        "migrate",
        help="Run content migration (placeholder)"
    )
    migrate_parser.add_argument(
        "--source",
        help="Source WordPress URL or export file"
    )
    migrate_parser.add_argument(
        "--target",
        help="Target database connection string"
    )
    
    return parser


def handle_hello_command(args: argparse.Namespace) -> None:
    """Handle the hello command."""
    message = f"Hello, {args.name}!"
    if args.verbose:
        print(f"[VERBOSE] Executing hello command with name: {args.name}")
    print(message)


def handle_migrate_command(args: argparse.Namespace) -> None:
    """Handle the migrate command (placeholder)."""
    if args.verbose:
        print("[VERBOSE] Executing migrate command")
    
    print("Content migration functionality coming soon!")
    if args.source:
        print(f"Source: {args.source}")
    if args.target:
        print(f"Target: {args.target}")


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        argv: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.verbose:
        print("[VERBOSE] F3RVA Content Migration CLI started")
    
    if args.command == "hello":
        handle_hello_command(args)
    elif args.command == "migrate":
        handle_migrate_command(args)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())