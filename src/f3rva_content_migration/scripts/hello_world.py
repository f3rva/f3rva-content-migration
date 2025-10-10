"""
Hello World Script

A simple hello world script for testing the CLI functionality.
This script can be run directly or through the CLI.
"""

import sys
import argparse
from typing import List, Optional


def greet(name: str = "World", enthusiastic: bool = False) -> str:
    """
    Generate a greeting message.
    
    Args:
        name: The name to greet
        enthusiastic: Whether to add extra enthusiasm
        
    Returns:
        A greeting message
    """
    greeting = f"Hello, {name}!"
    if enthusiastic:
        greeting += " 🎉"
    return greeting


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the hello world script.
    
    Args:
        argv: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        prog="hello-world",
        description="A simple hello world script for testing"
    )
    
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)"
    )
    
    parser.add_argument(
        "-e", "--enthusiastic",
        action="store_true",
        help="Add extra enthusiasm to the greeting"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args(argv)
    
    message = greet(args.name, args.enthusiastic)
    print(message)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())