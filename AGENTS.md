# AGENTS.md - Bingo Card Generator

## Project Overview

This is a Python project that generates Bingo cards as PNG images. It supports two content types:
- **Integers**: Random numbers from 0-100
- **Quotes**: Text quotes loaded from a newline-separated file

## Build/Run Commands

### Install Dependencies
```bash
pip install Pillow>=10.0.0
```

### Run the Generator
```bash
python3 bingo_generator.py --players 5 --type integers
python3 bingo_generator.py --players 3 --type quotes --inputfile quotes.txt
```

### Linting and Type Checking
```bash
# Format code (if black/ruff installed)
ruff format bingo_generator.py
ruff check bingo_generator.py --fix

# Type checking (if mypy installed)
mypy bingo_generator.py
```

### Running Tests
```bash
# If pytest is available
pytest tests/ -v
pytest tests/test_bingo.py -v  # Run single test file
pytest tests/ -k test_card_creation  # Run single test by name
```

## Code Style Guidelines

### General Principles
- Write clean, readable, and maintainable Python code
- Follow PEP 8 style guidelines
- Keep functions focused and small (single responsibility)
- Use descriptive names for variables and functions

### Imports
- Group imports in order: standard library, third-party, local
- Use absolute imports when possible
- Avoid wildcard imports (`from module import *`)

### Formatting
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines to separate functions and logical sections
- No trailing whitespace

### Type Annotations
- Use type hints for all function parameters and return values
- Use `typing.Optional` instead of `| None` for Python 3.9 compatibility
- Use concrete types when possible (e.g., `list[str]` instead of `List[str]`)

### Naming Conventions
| Element | Convention | Example |
|---------|-----------|---------|
| Modules | lowercase with underscores | `bingo_generator.py` |
| Classes | CapWords | `BingoCard` |
| Functions | lowercase with underscores | `generate_integers()` |
| Variables | lowercase with underscores | `content_count` |
| Constants | UPPERCASE with underscores | `FREE_SPACE` |
| Arguments | lowercase with underscores | `--inputfile` |

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Handle errors gracefully at the user level (CLI scripts)
- Let internal functions raise exceptions with clear messages
- Validate file paths exist before operations

### File Structure
```
workspace/
├── AGENTS.md           # This file
├── bingo_generator.py  # Main script
├── requirements.txt    # Dependencies
├── quotes.txt         # Sample quotes file (user-created)
└── bingo_cards/       # Output directory (generated)
```

### Documentation
- Add docstrings to all public functions and classes
- Use Google-style docstrings:
```python
def generate_integers(count: int) -> list[str]:
    """Generate a list of random integers as strings.

    Args:
        count: Number of integers to generate.

    Returns:
        List of string representations of integers.
    """
```

### Testing Guidelines
- Test file naming: `test_<module_name>.py`
- Test class naming: `Test<ClassName>`
- Test function naming: `test_<function_name>_<scenario>`
- Use descriptive assertion messages

### Dependencies
- Only add necessary dependencies
- Document minimum version requirements in `requirements.txt`
- Pillow is the only external dependency for image generation
