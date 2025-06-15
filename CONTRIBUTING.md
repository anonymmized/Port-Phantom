# Contributing to Port-Phantom

Thank you for your interest in contributing to Port-Phantom! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you are expected to uphold our values of:
- Respectful and inclusive communication
- Educational and responsible use of security tools
- Professional conduct in all interactions

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to see if the problem has already been reported.

**Bug Report Guidelines:**
- Use the bug report template
- Include detailed steps to reproduce the issue
- Provide system information (OS, Python version, etc.)
- Include error messages and logs
- Describe expected vs actual behavior

### Suggesting Enhancements

We welcome feature requests and enhancement suggestions.

**Enhancement Guidelines:**
- Use the feature request template
- Clearly describe the proposed feature
- Explain the use case and benefits
- Consider security implications
- Provide implementation suggestions if possible

### Pull Requests

We welcome pull requests for bug fixes and enhancements.

**PR Guidelines:**
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes
- Add tests if applicable
- Update documentation
- Commit with clear messages
- Push to your branch
- Create a Pull Request

**Commit Message Format:**
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## Development Setup

### Prerequisites
- Python 3.7+
- Git
- nmap (for network scanning)

### Local Development
1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
5. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_scanner.py
```

### Code Style
We use:
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting
- **mypy** for type checking

Run formatting:
```bash
black src/
isort src/
flake8 src/
mypy src/
```

## Project Structure

```
Port-Phantom/
├── src/                    # Source code
│   ├── config/            # Configuration
│   ├── scanners/          # Network scanning
│   ├── classifiers/       # Device classification
│   ├── core/             # Core logic
│   ├── reports/          # Report generation
│   └── utils/            # Utilities
├── config/               # Configuration files
├── data/                # Data files
├── tests/               # Test files
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

## Adding New Features

### Device Signatures
To add new device signatures:

1. Edit `config/signatures.yaml`
2. Add new signature with:
   - Name and description
   - Conditions (manufacturer, ports, device_type)
   - Risk level
   - CVE information

### Device Classifiers
To add new device classifiers:

1. Edit `src/classifiers/device_classifier.py`
2. Add classification logic
3. Update manufacturer lists in `src/config/settings.py`

### Risk Assessment Rules
To add new risk rules:

1. Edit `src/config/settings.py`
2. Add rules to `RISK_RULES` dictionary
3. Update risk calculation logic if needed

## Security Considerations

### Responsible Disclosure
- Report security vulnerabilities privately
- Provide detailed information about the issue
- Allow reasonable time for fixes
- Coordinate public disclosure

### Code Security
- Validate all user inputs
- Use secure defaults
- Avoid hardcoded credentials
- Follow security best practices

## Documentation

### Code Documentation
- Use docstrings for all functions and classes
- Follow Google docstring format
- Include examples for complex functions
- Document parameters and return values

### User Documentation
- Update README.md for new features
- Add usage examples
- Update CLI help text
- Maintain accurate installation instructions

## Testing

### Test Coverage
- Aim for >80% test coverage
- Test edge cases and error conditions
- Mock external dependencies
- Use fixtures for common test data

### Test Types
- Unit tests for individual functions
- Integration tests for modules
- End-to-end tests for complete workflows
- Performance tests for critical paths

## Release Process

### Version Bumping
- Use semantic versioning
- Update version in `__init__.py`
- Update CHANGELOG.md
- Tag releases in Git

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Release notes prepared
- [ ] Security review completed

## Getting Help

### Questions and Support
- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Join our community chat (if available)
- Contact maintainers for urgent issues

### Mentoring
- We welcome new contributors
- Ask for help with complex changes
- Request code reviews
- Participate in discussions

## Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Added to the contributors list
- Recognized for significant contributions

Thank you for contributing to Port-Phantom! 