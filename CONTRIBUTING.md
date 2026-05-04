# Contributing to WySlMtS

Thank you for your interest in contributing to WySlMtS! This project aims to be a high-quality, professional AI productivity tool.

## How to Contribute

1. **Reporting Bugs**: Use GitHub Issues to report bugs. Provide clear steps to reproduce.
2. **Feature Requests**: Open an issue to discuss new features before implementing them.
3. **Pull Requests**:
    - Ensure your code follows the existing style.
    - Add tests for new features or bug fixes.
    - Ensure all tests pass (`pytest`).
    - Keep commits small and descriptive.

## Development Setup

1. Clone the repo.
2. Install dependencies: `pip install -e ".[all]"`
3. Run tests: `pytest`

## Architecture

The project follows Clean Architecture principles. Logic is separated into:
- `models.py`: Data structures.
- `storage.py`: Persistence.
- `ai_service.py`: External AI integrations.
- `cli.py`: User interface.

Happy coding!
