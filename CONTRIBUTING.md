# Contributing to PC CamTouch

Thank you for your interest in contributing to PC CamTouch! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- VLC Media Player installed on your system
- Git

### Getting Started

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pyqt-on-camera.git
   cd pyqt-on-camera
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   # Install core dependencies
   pip install -r requirements.txt
   
   # (Optional) Install development dependencies
   pip install -e ".[dev]"
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

## Project Structure

```
pyqt-on-camera/
├── main.py                 # Application entry point
├── src/
│   ├── app.py              # Main application window
│   ├── widgets/            # UI components
│   ├── services/           # Business logic
│   └── models/             # Data models
├── docs/                   # Development documentation
├── data/                   # Local database (auto-created)
└── config/                 # User settings
```

## Development Phases

The project is organized into development phases. Please refer to the documentation in the `docs/` folder:

| Phase | Description | Status |
|-------|-------------|--------|
| [Phase 1](docs/phase-1-basic-setup.md) | Basic Setup - PyQt6, VLC, SQLite | In Progress |
| [Phase 2](docs/phase-2-core-features.md) | Core Features - Multi-camera, Stream management | Pending |
| [Phase 3](docs/phase-3-video-analysis.md) | Video Analysis - Metadata, Snapshots, Recording | Pending |
| [Phase 4](docs/phase-4-advanced-features.md) | Advanced - SRGAN, ICC integration, Custom layouts | Pending |

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists in [GitHub Issues](https://github.com/hoangnv170752/pyqt-on-camera/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, VLC version)

### Suggesting Features

1. Check existing issues and the development phases documentation
2. Create a new issue with the `enhancement` label
3. Describe the feature and its use case

### Submitting Pull Requests

1. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes:**
   ```bash
   python main.py  # Manual testing
   pytest          # Run automated tests (if available)
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter default)

### Formatting Tools

```bash
# Format code with Black
black src/ main.py

# Sort imports with isort
isort src/ main.py

# Check with flake8
flake8 src/ main.py
```

### Code Organization

- Keep widgets in `src/widgets/`
- Keep business logic in `src/services/`
- Keep data models in `src/models/`
- Use the logger from `src/services/logger.py` for logging

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Reference issue numbers when applicable: `Fix #123: Description`

## Testing

### Manual Testing

Always test your changes by running the application:

```bash
python main.py
```

### Automated Tests

When adding new features, consider adding tests:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_specific.py
```

## Questions?

If you have questions about contributing, please:

1. Check the documentation in `docs/`
2. Review existing issues and pull requests
3. Create a new issue with the `question` label

## License

By contributing to PC CamTouch, you agree that your contributions will be licensed under the MIT License.
