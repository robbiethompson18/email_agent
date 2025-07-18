# Email Unsubscribe Agent

A Python tool that automatically finds and unsubscribes from unwanted emails using the Gmail API and optional LLM assistance.

## Features

- **Email Finding**: Search for emails matching specific criteria in your Gmail account
- **Rule-Based Unsubscribing**: Find and follow unsubscribe links using pattern matching
- **LLM-Based Unsubscribing**: Use OpenAI's models to intelligently find unsubscribe links
- **FastAPI Backend**: Web API for email processing
- **Modular Design**: Separate components for authentication, email finding, and unsubscribing

## Setup

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/robbiethompson18/email_agent.git
   cd email_agent
   ```

2. **Install dependencies**
   
   **With uv (recommended):**
   ```bash
   uv sync
   ```
   
   **With pip:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Gmail API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Gmail API
   - Configure OAuth consent screen (add yourself as a test user)
   - Create OAuth client ID credentials (Desktop application)
   - Download the credentials JSON file and save as `keys/mcagent2.json`

4. **OpenAI API Key**
   - Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY="your_key_here"
   ```

## Usage

### Development workflow with uv

```bash
# Add new dependencies
uv add package-name

# Remove dependencies  
uv remove package-name

# Run scripts
uv run python src/main.py

# Run tests
uv run pytest

# Start FastAPI server
uv run uvicorn src.api:app --reload
```

### Running the application

**Command line:**
```bash
uv run python src/main.py
```

**Start the node frontend:**
npm run watch 
(from the frontend folder, will continuously compile )

**FastAPI server:**
```bash
uv run uvicorn src.api:app --reload --port 8000
```
Visit `http://localhost:8000/docs` for interactive API documentation.

**Tests:**
```bash
uv run pytest tests/
```

## Project Structure

```
email_project/
├── src/                    # Source code
│   ├── api.py             # FastAPI server
│   ├── email_finder.py    # Email search functionality
│   ├── unsubscribe_agent.py   # LLM-based unsubscribing
│   ├── openai_agent.py    # OpenAI API wrapper
│   └── shared_auth.py     # Gmail authentication
├── tests/                 # Test files
├── keys/                  # Credentials (gitignored)
├── .env                   # Environment variables (gitignored)
├── pyproject.toml         # Project configuration
└── README.md
```

## Note on Virtual Environments

This project uses `.venv/` (hidden directory) for virtual environments. The `.venv/` directory is automatically created by uv and should not be committed to git. When you clone this repository, run `uv sync` to recreate the virtual environment with all dependencies.