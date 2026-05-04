# WySlMtS - Personal AI Productivity CLI

![License](https://img.shields.io/github/license/YosefSafi/WySlMtS)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Build Status](https://github.com/YosefSafi/WySlMtS/actions/workflows/ci.yml/badge.svg)

WySlMtS (Work Your Smart Life, Manage the Stuff) is a professional, AI-powered command-line interface designed to supercharge your daily productivity.

## 🚀 Features

- **Intelligent Task Management**: Track tasks with priority, status, and local persistence.
- **AI Research Agent**: Real-time web search (via Tavily) and synthesis using GPT-4.
- **Daily Productivity Summaries**: AI-generated reports of your achievements and focus areas.
- **Interactive Shell Mode**: A polished interactive environment for seamless workflow.
- **Desktop Notifications**: Stay informed with system alerts for task and research events.
- **Configuration Management**: Manage API keys and AI models directly through the CLI.
- **CI/CD Ready**: Automated testing with GitHub Actions.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **CLI Framework**: [Typer](https://typer.tiangolo.com/) & [Rich](https://rich.readthedocs.io/)
- **Interactive Mode**: [Questionary](https://questionary.readthedocs.io/)
- **AI Integration**: [OpenAI GPT-4](https://openai.com/) & [Tavily Search](https://tavily.com/)
- **Persistence**: JSON-based local storage
- **Notifications**: [Plyer](https://plyer.readthedocs.io/)
- **Testing**: [Pytest](https://docs.pytest.org/)

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YosefSafi/WySlMtS.git
cd WySlMtS

# Install the package in editable mode
pip install -e .
```

## ⚙️ Configuration

Set up your API keys using the built-in config command:

```bash
wyslmts config set openai_api_key "your-key-here"
wyslmts config set tavily_api_key "your-key-here"
```

## 📖 Usage

### Interactive Mode (Recommended)
```bash
wyslmts interactive
```

### Standard Commands
```bash
# Tasks
wyslmts task add "Research clean architecture" --priority high
wyslmts task list
wyslmts task done <id-prefix>

# Research
wyslmts research topic "Future of AI Agents"

# Summary
wyslmts summary generate
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 🏗️ Architecture

The project follows a modular, clean design:

- `wyslmts.cli`: Entry point and command definitions.
- `wyslmts.models`: Pydantic data structures.
- `wyslmts.storage`: Local JSON persistence logic.
- `wyslmts.ai_service`: OpenAI and Tavily integration.
- `wyslmts.config`: User settings and preference management.
- `wyslmts.notifications`: Desktop alert system.
- `wyslmts.utils`: Shared helper functions.

## 📄 License

This project is licensed under the MIT License.
