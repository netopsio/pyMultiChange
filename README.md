pyMultiChange
=============

![CI](https://github.com/netopsio/pyMultiChange/workflows/CI/badge.svg)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

PyMultiChange is a modern Python application that allows you to make mass configuration changes to Cisco routers and switches. It utilizes the [netlib](https://github.com/netopsio/netlib) library for device connectivity.

## Features

- 🚀 **Python 3.10+** - Modern Python with type hints and latest features
- 📦 **Poetry** - Modern dependency management and packaging
- ✅ **Pydantic** - Robust input/output validation
- 🧪 **pytest** - Comprehensive test coverage
- 🔍 **Linting** - Ruff, Pylint, and MyPy for code quality
- 🔄 **GitHub Actions** - Automated CI/CD pipeline
- 🔌 **Multi-protocol** - Support for SSH and Telnet connections
- ⚡ **Threading** - Optional multi-threaded execution for faster operations

## Requirements

### System Dependencies

Netlib requires system packages for SNMP functionality:

#### Redhat/CentOS/Fedora
```bash
sudo yum install net-snmp-devel gcc python3-devel libffi-devel
```

#### Debian/Ubuntu
```bash
sudo apt-get install libsnmp-dev snmp-mibs-downloader gcc python3-dev libffi-dev
```

### Python Requirements

- Python 3.10 or higher
- Poetry for dependency management

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/netopsio/pyMultiChange.git
cd pyMultiChange

# Install with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/netopsio/pyMultiChange.git
cd pyMultiChange

# Install with pip
pip install .

## Usage

### First-time Setup

Set up your credentials in the system keyring:

```bash
multi-change -u your_username --set-creds
```

You'll be prompted to enter your password and enable password. These are securely stored in your system's keyring.

### Basic Usage

```bash
multi-change -u your_username -d hosts.txt -c commands.txt
```

### Command-line Options

```
usage: multi_change.py [-h] -u USERNAME [--delete-creds [DELETE_CREDS]]
                       [--set-creds [SET_CREDS]] [-d DEVICES] [-c COMMANDS]
                       [-s [SSH]] [-t [TELNET]] [-o [OUTPUT]] [-v [VERBOSE]]
                       [--delay DELAY] [--buffer BUFFER]
                       [--threaded [THREADED]] [-m MAXTHREADS]

Managing network devices with Python

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Specify your username
  --delete-creds        Delete credentials from keyring
  --set-creds           Set keyring credentials
  -d DEVICES, --devices DEVICES
                        Path to hosts file
  -c COMMANDS, --commands COMMANDS
                        Path to commands file
  -s [SSH], --ssh [SSH]
                        Use SSH protocol (default)
  -t [TELNET], --telnet [TELNET]
                        Use Telnet protocol
  -o [OUTPUT], --output [OUTPUT]
                        Show verbose command output
  -v [VERBOSE], --verbose [VERBOSE]
                        Enable debug logging
  --delay DELAY         Delay between commands in seconds (default: 2)
  --buffer BUFFER       SSH buffer size (default: 8192)
  --threaded            Enable multi-threaded execution
  -m MAXTHREADS, --maxthreads MAXTHREADS
                        Maximum number of threads (default: 10)
```

### Examples

#### Execute commands on multiple devices

```bash
# Create a hosts file
cat > hosts.txt << EOF
router1.example.com
router2.example.com
switch1.example.com
EOF

# Create a commands file
cat > commands.txt << EOF
show version
show running-config
show ip interface brief
EOF

# Run the commands
multi-change -u admin -d hosts.txt -c commands.txt
```

#### Use threading for faster execution

```bash
multi-change -u admin -d hosts.txt -c commands.txt --threaded -m 5
```

#### Show command output

```bash
multi-change -u admin -d hosts.txt -c commands.txt -o
```

#### Use Telnet instead of SSH

```bash
multi-change -u admin -d hosts.txt -c commands.txt -t
```

#### Enable debug logging

```bash
multi-change -u admin -d hosts.txt -c commands.txt -v
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/netopsio/pyMultiChange.git
cd pyMultiChange

# Install dependencies including dev dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=pymultichange

# Run specific test file
poetry run pytest tests/test_models.py
```

### Code Quality

```bash
# Run Ruff linter
poetry run ruff check .

# Run Ruff formatter
poetry run ruff format .

# Run Pylint
poetry run pylint pymultichange

# Run MyPy type checker
poetry run mypy pymultichange
```

### Running All Checks

```bash
# Run linting and tests
poetry run ruff check .
poetry run pylint pymultichange
poetry run mypy pymultichange
poetry run pytest
```

## Project Structure

```
pyMultiChange/
├── pymultichange/          # Main package
│   ├── __init__.py
│   ├── models.py           # Pydantic models for validation
│   └── multi_change.py     # Main application logic
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_models.py      # Model tests
│   └── test_multi_change.py # Application tests
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD
├── pyproject.toml          # Poetry configuration
├── mypy.ini               # MyPy configuration
├── .pylintrc              # Pylint configuration
├── .ruff.toml             # Ruff configuration
└── README.md              # This file
```

## CI/CD

This project uses GitHub Actions for continuous integration. On each push and pull request, the following checks run:

- ✅ Linting with Ruff
- ✅ Type checking with MyPy
- ✅ Code quality with Pylint
- ✅ Tests with pytest across Python 3.10, 3.11, and 3.12
- ✅ Build verification

## Contributing

Contributions are welcome! Please ensure your code:

1. Passes all linting checks (Ruff, Pylint, MyPy)
2. Includes tests for new functionality
3. Maintains or improves test coverage
4. Follows the existing code style

## License

This project is open source. Please check the repository for license details.

## Credits

- Original author: James Williams
- Modernization: Updated for Python 3.10+ with modern tooling
- Uses [netlib](https://github.com/netopsio/netlib) for device connectivity
