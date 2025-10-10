"""
Test the CLI module functionality.
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from f3rva_content_migration.cli import main, create_parser
from f3rva_content_migration.scripts.hello_world import greet


def test_parser_creation():
    """Test that the parser is created correctly."""
    parser = create_parser()
    assert parser.prog == "f3rva-migrate"
    print("✓ Parser creation test passed")


def test_hello_command_basic():
    """Test the hello command with basic functionality."""
    result = main(["hello"])
    assert result == 0
    print("✓ Hello command basic test passed")


def test_hello_command_with_name():
    """Test the hello command with custom name."""
    result = main(["hello", "Test"])
    assert result == 0
    print("✓ Hello command with name test passed")


def test_hello_command_verbose():
    """Test the hello command with verbose flag."""
    result = main(["--verbose", "hello", "Test"])
    assert result == 0
    print("✓ Hello command verbose test passed")


def test_migrate_command():
    """Test the migrate command placeholder."""
    result = main(["migrate"])
    assert result == 0
    print("✓ Migrate command test passed")


def test_no_command():
    """Test CLI with no command shows help."""
    result = main([])
    assert result == 1
    print("✓ No command test passed")


def test_hello_world_script():
    """Test the hello world script functions."""
    # Test basic greeting
    assert greet() == "Hello, World!"
    assert greet("Test") == "Hello, Test!"
    assert greet("Test", enthusiastic=True) == "Hello, Test! 🎉"
    print("✓ Hello world script test passed")


def run_all_tests():
    """Run all tests."""
    print("Running CLI functionality tests...")
    print()
    
    try:
        test_parser_creation()
        test_hello_command_basic()
        test_hello_command_with_name()
        test_hello_command_verbose()
        test_migrate_command()
        test_no_command()
        test_hello_world_script()
        
        print()
        print("🎉 All tests passed successfully!")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)