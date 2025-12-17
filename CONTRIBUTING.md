# Contributing to Mac Cleaner

Thank you for your interest in contributing to Mac Cleaner! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- macOS 10.13 or later
- Python 3.8 or later
- Git
- Optional: gettext (for translation work)

### Setting Up Development Environment

1. Fork the repository on GitHub

2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/mac-cleaner.git
   cd mac-cleaner
   ```

3. Install in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Running the Application

During development, you can run the application directly:

```bash
python -m mac_cleaner.cleaner
```

Or if installed:

```bash
mac-cleaner
```

### Code Style

We use Black for code formatting:

```bash
black mac_cleaner/
```

### Type Checking

We use mypy for type checking:

```bash
mypy mac_cleaner/
```

### Running Tests

Run tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mac_cleaner --cov-report=html

# Run specific test file
pytest tests/test_cleaner.py -v
```

## Working with Translations

### Adding a New Language

1. Create a new directory for the language:
   ```bash
   mkdir -p mac_cleaner/locales/fr_FR/LC_MESSAGES
   ```

2. Copy the template:
   ```bash
   cp mac_cleaner/locales/mac_cleaner.pot \
      mac_cleaner/locales/fr_FR/LC_MESSAGES/mac_cleaner.po
   ```

3. Edit the `.po` file and translate the strings

4. Compile translations:
   ```bash
   python compile_translations.py
   ```

### Updating Existing Translations

1. Edit the `.po` file in `mac_cleaner/locales/*/LC_MESSAGES/`

2. Compile translations:
   ```bash
   python compile_translations.py
   ```

### Extracting New Strings

If you've added new translatable strings to the code:

1. Update the `.pot` template file manually, or use:
   ```bash
   # Install gettext first: brew install gettext
   xgettext -d mac_cleaner -o mac_cleaner/locales/mac_cleaner.pot \
            mac_cleaner/*.py
   ```

2. Update each language's `.po` file with the new strings

## Making Changes

### Code Guidelines

1. **Safety First**: Any changes that involve file deletion must include safety checks
2. **Documentation**: Update docstrings and README as needed
3. **Tests**: Add tests for new functionality
4. **Type Hints**: Use type hints for function parameters and return values
5. **Comments**: Add comments for complex logic

### Safety Considerations

When working on file deletion logic:

- Always test with `--dry-run` first
- Add paths to `CRITICAL_PATHS` if they should never be deleted
- Use `is_safe_to_delete()` before any deletion
- Add appropriate error handling
- Test thoroughly on a non-production system

### Commit Messages

Use clear, descriptive commit messages:

```
Add support for cleaning Rust target directories

- Add ~/.cargo/target to Development Cache category
- Update tests to verify Rust cache detection
- Update README with Rust cache information
```

## Submitting Changes

1. Ensure all tests pass:
   ```bash
   pytest
   ```

2. Ensure code is formatted:
   ```bash
   black mac_cleaner/
   ```

3. Update documentation if needed

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request on GitHub

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation as needed
- Keep changes focused and atomic

## Reporting Issues

When reporting issues, please include:

- macOS version
- Python version
- Mac Cleaner version
- Steps to reproduce
- Expected vs actual behavior
- Any error messages or logs

## Questions?

Feel free to open an issue for questions or discussions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
