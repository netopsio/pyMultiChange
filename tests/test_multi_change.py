"""Tests for main multi_change module."""

from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from pymultichange.models import DeviceSettings, Protocol
from pymultichange.multi_change import (
    log_failure,
    read_file_lines,
    setup_logging,
)


class TestSetupLogging:
    """Test logging setup."""

    def test_setup_logging_verbose(self) -> None:
        """Test logging setup with verbose mode."""
        setup_logging(verbose=True)
        # Just verify it doesn't raise an exception

    def test_setup_logging_non_verbose(self) -> None:
        """Test logging setup without verbose mode."""
        setup_logging(verbose=False)
        # Just verify it doesn't raise an exception


class TestLogFailure:
    """Test failure logging."""

    def test_log_failure_creates_file(self, tmp_path: Path) -> None:
        """Test that log_failure creates a new file."""
        log_file = tmp_path / "test_failure.log"
        log_failure("router1.example.com", str(log_file))
        assert log_file.exists()
        assert log_file.read_text() == "router1.example.com\n"

    def test_log_failure_appends_to_existing(self, tmp_path: Path) -> None:
        """Test that log_failure appends to existing file."""
        log_file = tmp_path / "test_failure.log"
        log_failure("router1.example.com", str(log_file))
        log_failure("router2.example.com", str(log_file))

        content = log_file.read_text()
        assert "router1.example.com\n" in content
        assert "router2.example.com\n" in content


class TestReadFileLines:
    """Test file reading utilities."""

    def test_read_file_lines_success(self, tmp_path: Path) -> None:
        """Test successful file reading."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\n  line3  \n\nline4\n")

        lines = read_file_lines(str(test_file), "test")
        assert lines == ["line1", "line2", "line3", "line4"]

    def test_read_file_lines_nonexistent(self) -> None:
        """Test reading nonexistent file raises SystemExit."""
        with pytest.raises(SystemExit):
            read_file_lines("/nonexistent/file.txt", "test")

    def test_read_file_lines_empty(self, tmp_path: Path) -> None:
        """Test reading empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")

        lines = read_file_lines(str(test_file), "test")
        assert lines == []


class TestDeviceConnection:
    """Test device connection functionality."""

    @patch("pymultichange.multi_change.SSH")
    def test_device_connection_ssh_success(self, mock_ssh: Mock) -> None:
        """Test successful SSH connection."""
        from pymultichange.multi_change import device_connection

        # Setup mock
        mock_conn = MagicMock()
        mock_ssh.return_value = mock_conn
        mock_conn.command.return_value = "output"

        # Create device settings
        settings = DeviceSettings(
            device_name="router1.example.com",
            protocol=Protocol.SSH,
            username="testuser",
            password="testpass",
            enable_password="enablepass",
            commands=["show version"],
        )

        # Execute
        device_connection(settings)

        # Verify
        mock_ssh.assert_called_once()
        mock_conn.connect.assert_called_once()
        mock_conn.set_enable.assert_called_once_with("enablepass")
        mock_conn.disable_paging.assert_called_once()
        mock_conn.command.assert_called_once_with("show version")
        mock_conn.close.assert_called_once()

    @patch("pymultichange.multi_change.Telnet")
    def test_device_connection_telnet_success(self, mock_telnet: Mock) -> None:
        """Test successful Telnet connection."""
        from pymultichange.multi_change import device_connection

        # Setup mock
        mock_conn = MagicMock()
        mock_telnet.return_value = mock_conn
        mock_conn.command.return_value = "output"

        # Create device settings
        settings = DeviceSettings(
            device_name="router1.example.com",
            protocol=Protocol.TELNET,
            username="testuser",
            password="testpass",
            enable_password="enablepass",
            commands=["show version"],
        )

        # Execute
        device_connection(settings)

        # Verify
        mock_telnet.assert_called_once()
        mock_conn.connect.assert_called_once()
        mock_conn.set_enable.assert_called_once_with("enablepass")
        mock_conn.disable_paging.assert_called_once()
        mock_conn.command.assert_called_once_with("show version")
        mock_conn.close.assert_called_once()

    @patch("pymultichange.multi_change.SSH")
    @patch("pymultichange.multi_change.log_failure")
    def test_device_connection_failure(self, mock_log_failure: Mock, mock_ssh: Mock) -> None:
        """Test handling of connection failure."""
        from pymultichange.multi_change import device_connection

        # Setup mock to raise exception
        mock_ssh.side_effect = Exception("Connection failed")

        # Create device settings
        settings = DeviceSettings(
            device_name="router1.example.com",
            protocol=Protocol.SSH,
            username="testuser",
            password="testpass",
            enable_password="enablepass",
            commands=["show version"],
        )

        # Execute (should not raise exception)
        device_connection(settings)

        # Verify failure was logged
        mock_log_failure.assert_called_once_with("router1.example.com")
