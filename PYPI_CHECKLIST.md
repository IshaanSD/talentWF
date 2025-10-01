# PyPI Publishing Checklist

## Pre-Publication Checklist

### ✅ Package Configuration
- [ ] Update `pyproject.toml` with correct author information
- [ ] Update `pyproject.toml` with correct email address
- [ ] Update GitHub URLs in `pyproject.toml` (if applicable)
- [ ] Verify version number in `pyproject.toml`
- [ ] Check that all dependencies are correctly specified
- [ ] Verify package name is unique on PyPI

### ✅ Documentation
- [ ] README.md is complete and accurate
- [ ] Installation instructions are correct
- [ ] Usage examples work
- [ ] API documentation is clear
- [ ] LICENSE file is present and correct

### ✅ Code Quality
- [ ] All tests pass: `pytest tests/`
- [ ] No linting errors: `flake8 src/ tests/`
- [ ] Code follows PEP 8 style guidelines
- [ ] All imports work correctly
- [ ] Package can be imported: `from talenWF import FindTALTask`

### ✅ Build and Test
- [ ] Package builds successfully: `python -m build`
- [ ] Package passes twine check: `python -m twine check dist/*`
- [ ] Package installs correctly: `pip install dist/talenWF-*.whl`
- [ ] CLI works after installation: `talenWF-findtal --help`
- [ ] API works after installation: `python -c "from talenWF import FindTALTask"`

## PyPI Accounts Setup

### ✅ Test PyPI Account
- [ ] Create account at https://test.pypi.org/account/register/
- [ ] Generate API token
- [ ] Configure `~/.pypirc` with test token

### ✅ Production PyPI Account
- [ ] Create account at https://pypi.org/account/register/
- [ ] Generate API token
- [ ] Configure `~/.pypirc` with production token

## Publishing Process

### ✅ Test Upload
- [ ] Upload to Test PyPI: `python -m twine upload --repository testpypi dist/*`
- [ ] Test installation from Test PyPI
- [ ] Verify package works correctly

### ✅ Production Upload
- [ ] Upload to PyPI: `python -m twine upload dist/*`
- [ ] Test installation from PyPI: `pip install talenWF`
- [ ] Verify package works correctly

## Post-Publication

### ✅ Verification
- [ ] Package appears on PyPI: https://pypi.org/project/talenWF/
- [ ] Installation works: `pip install talenWF`
- [ ] CLI works: `talenWF-findtal --help`
- [ ] API works: `from talenWF import FindTALTask`

### ✅ Documentation Updates
- [ ] Update any external documentation
- [ ] Create GitHub release (if applicable)
- [ ] Update any project websites

## Quick Commands

```bash
# Build and check
python -m build
python -m twine check dist/*

# Test upload
python -m twine upload --repository testpypi dist/*

# Production upload
python -m twine upload dist/*

# Test installation
pip install talenWF
```

## Troubleshooting

- **Package name exists**: Choose a different name
- **Version exists**: Increment version number
- **Authentication fails**: Check API tokens in `~/.pypirc`
- **Build fails**: Check `pyproject.toml` syntax
- **Import fails**: Check package structure and `__init__.py`
