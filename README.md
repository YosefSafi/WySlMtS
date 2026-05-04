# WySlMtS - Personal AI Productivity CLI

![License](https://img.shields.io/github/license/YosefSafi/WySlMtS)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Build Status](https://img.shields.io/github/actions/workflow/status/YosefSafi/WySlMtS/ci.yml?branch=main)

A professional, AI-powered command-line interface designed to supercharge your daily productivity. Features include intelligent task management, an automated research agent, and insightful daily summaries.

## 🚀 Features

- **Task Management**: Intelligent task tracking with priority and context awareness.
- **Research Agent**: Deep-dive into topics using AI-driven web search and synthesis.
- **Daily Summaries**: Automatically generated reports of your achievements and upcoming focus areas.
- **Clean Architecture**: Built with modularity and extensibility in mind.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **CLI Framework**: Typer / Click
- **AI Integration**: OpenAI / Anthropic API
- **Testing**: Pytest
- **Linting/Formatting**: Ruff

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YosefSafi/WySlMtS.git
cd WySlMtS

# Install dependencies (using poetry or pip)
pip install -e .
```

## 📖 Usage

```bash
# Add a task
wyslmts task add "Research clean architecture" --priority high

# Start a research session
wyslmts research "Best practices for CLI design"

# Generate daily summary
wyslmts summary generate
```

## 🏗️ Architecture

The project follows a modular design inspired by Clean Architecture:

- **Models**: Defines the data structures (Tasks, Priority) using Pydantic.
- **Storage**: Handles local JSON persistence.
- **AI Service**: Encapsulates OpenAI API logic for research and summaries.
- **CLI**: The interface layer using Typer and Rich for a polished user experience.

```
src/wyslmts/
├── cli.py          # CLI commands and entry point
├── models.py       # Pydantic data models
├── storage.py      # Local JSON storage logic
└── ai_service.py   # OpenAI integration
```

## 🧪 Testing

Run tests using pytest:

```bash
pytest
```

## 🤝 Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
