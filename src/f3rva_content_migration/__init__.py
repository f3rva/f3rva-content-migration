"""
F3RVA Content Migration Library

A Python library for migrating content from WordPress to structured databases.
"""

__version__ = "0.1.0"
__author__ = "F3 RVA"
__email__ = "info@f3rva.com"

from .cli import main as cli_main

__all__ = ["cli_main"]