# Git & Environment Setup

## How to Reproduce the Environment

Follow these steps to set up your development environment and CI:

1. **Clone the repository:**

    git clone https://github.com/Seya-prog/solar-challenge-week1.git
    cd solar-challenge-week1


2. **Set up a Python virtual environment:**

    python -m venv .venv
    # On Unix/macOS:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    

3. **Install dependencies:**

    pip inastall pandas
    

4. **Continuous Integration:**
    - This project uses GitHub Actions for CI.
    - On every push or pull request, the workflow in `.github/workflows/ci.yml` will:
        - Set up Python 3.11
        - Install dependencies from `requirements.txt`
        - Run `python --version` to verify the environment

5. **.gitignore:**
    - The `.gitignore` file excludes virtual environments, data directories, and notebook checkpoints.

## Folder Structure

solar-challenge-week1/
│
├── .github/
│   └── workflows/
│       └── ci.yml
├── .vscode/
│   └── settings.json
├── src/
│   ├── notebooks/
│   └── scripts/
│   └── tests/
├── requirements.txt
├── .gitignore
└── README.md

For more details, see the [ci.yml](.github/workflows/ci.yml) workflow file.
