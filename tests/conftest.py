"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
from typing import Generator


@pytest.fixture
def temp_hosts_file(tmp_path: Path) -> Path:
    """Create a temporary hosts file for testing."""
    hosts_file = tmp_path / "hosts.txt"
    hosts_file.write_text("router1.example.com\nrouter2.example.com\nswitch1.example.com\n")
    return hosts_file


@pytest.fixture
def temp_commands_file(tmp_path: Path) -> Path:
    """Create a temporary commands file for testing."""
    commands_file = tmp_path / "commands.txt"
    commands_file.write_text("show version\nshow running-config\nshow ip interface brief\n")
    return commands_file


@pytest.fixture
def mock_credentials() -> dict[str, str]:
    """Return mock credentials for testing."""
    return {
        "username": "testuser",
        "password": "testpass",
        "enable": "enablepass",
    }
