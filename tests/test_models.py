"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from pymultichange.models import Arguments, Credentials, DeviceSettings, Protocol


class TestCredentials:
    """Test Credentials model."""

    def test_valid_credentials(self) -> None:
        """Test creating valid credentials."""
        creds = Credentials(
            username="testuser",
            password="testpass",
            enable="enablepass",
        )
        assert creds.username == "testuser"
        assert creds.password == "testpass"
        assert creds.enable == "enablepass"

    def test_empty_username_fails(self) -> None:
        """Test that empty username raises validation error."""
        with pytest.raises(ValidationError):
            Credentials(username="", password="testpass", enable="enablepass")

    def test_empty_password_fails(self) -> None:
        """Test that empty password raises validation error."""
        with pytest.raises(ValidationError):
            Credentials(username="testuser", password="", enable="enablepass")

    def test_empty_enable_fails(self) -> None:
        """Test that empty enable password raises validation error."""
        with pytest.raises(ValidationError):
            Credentials(username="testuser", password="testpass", enable="")


class TestDeviceSettings:
    """Test DeviceSettings model."""

    def test_valid_device_settings(self) -> None:
        """Test creating valid device settings."""
        settings = DeviceSettings(
            device_name="router1.example.com",
            protocol=Protocol.SSH,
            username="testuser",
            password="testpass",
            enable_password="enablepass",
            delay=2,
            buffer=8192,
            commands=["show version"],
            command_output=True,
        )
        assert settings.device_name == "router1.example.com"
        assert settings.protocol == Protocol.SSH
        assert settings.delay == 2
        assert settings.buffer == 8192
        assert len(settings.commands) == 1

    def test_default_values(self) -> None:
        """Test default values are applied correctly."""
        settings = DeviceSettings(
            device_name="router1.example.com",
            username="testuser",
            password="testpass",
            enable_password="enablepass",
        )
        assert settings.protocol == Protocol.SSH
        assert settings.delay == 2
        assert settings.buffer == 8192
        assert settings.commands == []
        assert settings.command_output is False

    def test_device_name_stripped(self) -> None:
        """Test that device name is stripped of whitespace."""
        settings = DeviceSettings(
            device_name="  router1.example.com  ",
            username="testuser",
            password="testpass",
            enable_password="enablepass",
        )
        assert settings.device_name == "router1.example.com"

    def test_empty_device_name_fails(self) -> None:
        """Test that empty device name raises validation error."""
        with pytest.raises(ValidationError):
            DeviceSettings(
                device_name="   ",
                username="testuser",
                password="testpass",
                enable_password="enablepass",
            )

    def test_negative_delay_fails(self) -> None:
        """Test that negative delay raises validation error."""
        with pytest.raises(ValidationError):
            DeviceSettings(
                device_name="router1.example.com",
                username="testuser",
                password="testpass",
                enable_password="enablepass",
                delay=-1,
            )

    def test_invalid_buffer_fails(self) -> None:
        """Test that buffer below minimum raises validation error."""
        with pytest.raises(ValidationError):
            DeviceSettings(
                device_name="router1.example.com",
                username="testuser",
                password="testpass",
                enable_password="enablepass",
                buffer=512,
            )


class TestProtocol:
    """Test Protocol enum."""

    def test_ssh_protocol(self) -> None:
        """Test SSH protocol value."""
        assert Protocol.SSH.value == "ssh"

    def test_telnet_protocol(self) -> None:
        """Test Telnet protocol value."""
        assert Protocol.TELNET.value == "telnet"

    def test_protocol_comparison(self) -> None:
        """Test protocol comparison."""
        assert Protocol.SSH == Protocol.SSH
        assert Protocol.SSH != Protocol.TELNET


class TestArguments:
    """Test Arguments model."""

    def test_valid_arguments(self) -> None:
        """Test creating valid arguments."""
        args = Arguments(
            username="testuser",
            devices="/path/to/hosts",
            commands="/path/to/commands",
            verbose=True,
        )
        assert args.username == "testuser"
        assert args.devices == "/path/to/hosts"
        assert args.commands == "/path/to/commands"
        assert args.verbose is True

    def test_default_protocol_is_ssh(self) -> None:
        """Test that default protocol is SSH."""
        args = Arguments(username="testuser")
        assert args.protocol == Protocol.SSH

    def test_default_values(self) -> None:
        """Test default values are applied correctly."""
        args = Arguments(username="testuser")
        assert args.delay == "2"
        assert args.buffer == "8192"
        assert args.maxthreads == "10"
