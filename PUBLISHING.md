# Publishing Mac Cleaner to PyPI

This guide explains how to publish the Mac Cleaner package to PyPI so others can install it with `pip install mac-cleaner`.

## Prerequisites

1. **PyPI Account**
   - Create an account at https://pypi.org/account/register/
   - Verify your email

2. **TestPyPI Account** (for testing)
   - Create an account at https://test.pypi.org/account/register/

3. **Install Build Tools**
   ```bash
   pip install --upgrade build twine
   ```

## Step 1: Update Package Information

Before publishing, update these files:

### pyproject.toml
- Update `version` (follow semantic versioning: MAJOR.MINOR.PATCH)
- Update `authors` with your name and email
- Update URLs to point to your repository

Example:
```toml
version = "1.0.0"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]

[project.urls]
Homepage = "https://github.com/yourusername/mac-cleaner"
"Bug Reports" = "https://github.com/yourusername/mac-cleaner/issues"
"Source" = "https://github.com/yourusername/mac-cleaner"
```

### mac_cleaner/__init__.py
Update version and author:
```python
__version__ = "1.0.0"
__author__ = "Your Name"
```

## Step 2: Prepare the Package

1. **Clean previous builds**
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Ensure translations are compiled**
   ```bash
   python compile_translations.py
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Check code quality** (optional but recommended)
   ```bash
   black mac_cleaner/
   mypy mac_cleaner/
   ```

## Step 3: Build the Package

```bash
python -m build
```

This creates two files in the `dist/` directory:
- `mac-cleaner-1.0.0.tar.gz` (source distribution)
- `mac-cleaner-1.0.0-py3-none-any.whl` (wheel distribution)

## Step 4: Test on TestPyPI (Recommended)

1. **Upload to TestPyPI**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

2. **Enter your TestPyPI credentials**

3. **Test installation from TestPyPI**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ mac-cleaner
   ```

4. **Test the installed package**
   ```bash
   mac-cleaner --help
   mac-cleaner --dry-run
   ```

5. **Uninstall test version**
   ```bash
   pip uninstall mac-cleaner
   ```

## Step 5: Publish to PyPI

If everything works on TestPyPI:

1. **Upload to PyPI**
   ```bash
   python -m twine upload dist/*
   ```

2. **Enter your PyPI credentials**

3. **Verify on PyPI**
   - Visit https://pypi.org/project/mac-cleaner/
   - Check that all information is correct

4. **Test installation**
   ```bash
   pip install mac-cleaner
   mac-cleaner --version
   ```

## Step 6: Tag the Release on GitHub

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Create a release on GitHub with release notes.

## Using API Tokens (Recommended)

Instead of username/password, use API tokens:

1. **Create token on PyPI**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Scope it to "Entire account" or specific project

2. **Create ~/.pypirc**
   ```ini
   [pypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmc...  # Your token here

   [testpypi]
   username = __token__
   password = pypi-AgENdGVzdC5weXBpLm9y...  # Your TestPyPI token
   ```

3. **Set permissions**
   ```bash
   chmod 600 ~/.pypirc
   ```

## Updating the Package

When you need to publish an update:

1. **Make your changes**

2. **Update version number** in:
   - `pyproject.toml`
   - `mac_cleaner/__init__.py`

3. **Update CHANGELOG** (create one if it doesn't exist)

4. **Run tests**
   ```bash
   pytest
   ```

5. **Build and upload**
   ```bash
   rm -rf dist/
   python -m build
   python -m twine upload dist/*
   ```

6. **Tag the release**
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   git push origin v1.0.1
   ```

## Version Numbering

Follow semantic versioning (https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backwards compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backwards compatible

Examples:
- Bug fix: `1.0.0` → `1.0.1`
- New feature: `1.0.0` → `1.1.0`
- Breaking change: `1.0.0` → `2.0.0`

## Troubleshooting

### "Package already exists"
- You can't upload the same version twice
- Increment the version number

### "Invalid distribution file"
- Make sure to build fresh: `rm -rf dist/ && python -m build`
- Check that both `.tar.gz` and `.whl` files are present

### "Package name already taken"
- Choose a different package name
- Update `name` in `pyproject.toml`

### "README rendering failed"
- Test your README: `python -m twine check dist/*`
- Fix any markdown issues

## Checklist Before Publishing

- [ ] All tests pass
- [ ] Version number updated
- [ ] README is complete and accurate
- [ ] Author information is correct
- [ ] URLs point to correct repository
- [ ] Translations are compiled
- [ ] Package builds without errors
- [ ] Tested on TestPyPI
- [ ] LICENSE file is included
- [ ] CHANGELOG is updated

## After Publishing

1. **Announce the release**
   - Create a GitHub release
   - Update your README with installation instructions
   - Share on social media if desired

2. **Monitor for issues**
   - Watch for bug reports
   - Respond to questions

3. **Plan next version**
   - Collect feature requests
   - Prioritize improvements

## Resources

- PyPI: https://pypi.org/
- TestPyPI: https://test.pypi.org/
- Python Packaging Guide: https://packaging.python.org/
- Semantic Versioning: https://semver.org/
- Twine Documentation: https://twine.readthedocs.io/
