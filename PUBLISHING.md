# Publishing talenWF to PyPI

This guide walks you through publishing the talenWF package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - [Test PyPI](https://test.pypi.org/account/register/) (for testing)
   - [PyPI](https://pypi.org/account/register/) (for production)

2. **API Tokens**: Generate API tokens for both sites:
   - Go to Account Settings → API tokens
   - Create a new token with appropriate scope

3. **Install Build Tools**:
   ```bash
   pip install build twine
   ```

## Step-by-Step Publishing Process

### 1. Update Package Metadata

Before publishing, update the following in `pyproject.toml`:

- Replace `"Your Name"` with your actual name
- Replace `"your.email@example.com"` with your email
- Update GitHub URLs if you have a repository
- Update version number for new releases

### 2. Test the Package Locally

```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Test the CLI
talenWF-findtal --help

# Test the API
python check_package.py
```

### 3. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

This creates:
- `dist/talenWF-0.1.0-py3-none-any.whl` (wheel)
- `dist/talenWF-0.1.0.tar.gz` (source distribution)

### 4. Test on Test PyPI First

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ talenWF
```

### 5. Publish to Production PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

### 6. Verify Installation

```bash
# Install from PyPI
pip install talenWF

# Test the package
python -c "from talenWF import FindTALTask; print('Success!')"
```

## Authentication

### Option 1: API Token (Recommended)

Create `~/.pypirc`:
```ini
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

### Option 2: Username/Password

```bash
# For Test PyPI
python -m twine upload --repository testpypi --username your-username dist/*

# For Production PyPI
python -m twine upload --username your-username dist/*
```

## Version Management

For subsequent releases:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` (if you have one)
3. Build and upload again

```bash
# Example version bump
# Change version = "0.1.0" to version = "0.1.1" in pyproject.toml

python -m build
python -m twine upload dist/*
```

## Troubleshooting

### Common Issues:

1. **Package name already exists**: Choose a different name
2. **Version already exists**: Increment version number
3. **Authentication failed**: Check API tokens
4. **Build fails**: Check `pyproject.toml` syntax

### Useful Commands:

```bash
# Check package contents
python -m build --sdist --wheel
twine check dist/*

# Validate package
python -m build
python -m twine check dist/*

# Install from local build
pip install dist/talenWF-0.1.0-py3-none-any.whl
```

## Post-Publication

After successful publication:

1. **Test installation**: `pip install talenWF`
2. **Update documentation**: Update README with PyPI installation instructions
3. **Create GitHub release**: Tag the version in your repository
4. **Announce**: Share on relevant forums, social media, etc.

## Security Notes

- Never commit API tokens to version control
- Use `.pypirc` file with proper permissions (600)
- Consider using environment variables for CI/CD

## Example Commands Summary

```bash
# Complete workflow
cd /path/to/talenWF
pip install build twine
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ talenWF
python -m twine upload dist/*
pip install talenWF
```
